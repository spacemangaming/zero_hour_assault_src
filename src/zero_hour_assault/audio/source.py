from rotation import calculate_theta, get_3d_distance
import globals as g
from sound import sound

_LAZY_INIT_DIST = 120  # load audio when player comes within this many units

class source:
    def __init__(
        self,
        source_lx,
        source_rx,
        source_miny,
        source_maxy,
        source_minz,
        source_maxz,
        file,
        source_paused=False,
        source_id=-1, volume=0
    ):
        self.lx = source_lx
        self.volume = volume
        self.rx = source_rx
        self.miny = source_miny
        self.maxy = source_maxy
        self.minz = source_minz
        self.maxz = source_maxz
        self.soundfile = file
        self.id = source_id
        self.paused = source_paused
        self.p2 = source_paused
        self.source_sound = None
        self._audio_ready = False
        # Always defer — audio loads when player walks into range via sourcecheckloop

    def _load_audio(self):
        if self._audio_ready:
            return
        self._audio_ready = True
        self.source_sound = g.p.play_3d(
            self.soundfile,
            g.me.x, g.me.y, g.me.z,
            self.lx, self.miny, self.minz,
            calculate_theta(g.facing),
            True, False, True
        )
        try: self.source_sound.handle.volume = self.volume
        except: pass
        if self.paused:
            g.p.pause_sound(self.source_sound)
        self.p2 = self.paused
        g.p.update_sound_range_3d(
            self.source_sound,
            0, self.rx - self.lx,
            0, self.maxy - self.miny,
            0, self.maxz - self.minz,
            calculate_theta(g.facing),
        )


class amb:
    def __init__(self, c1, c2, c3, c4, c5, c6, so, vol=0):
        self.minx = c1
        self.volume=vol
        self.maxx = c2
        self.miny = c3
        self.maxy = c4
        self.minz = c5
        self.maxz = c6
        self.loop = sound()
        self.loop.load(so)
        self.loop.volume=self.volume
        self.inrange = False
        self.force_paused = False
        self.loop.player.stationary=True

    def is_in_range(self):
        if g.get_ignore_ambience_at(g.me.x,g.me.y,g.me.z): return False
        return (
            self.minx <= round(g.mr.x)
            and self.maxx >= round(g.mr.x)
            and self.miny <= round(g.mr.y)
            and self.maxy >= round(g.mr.y)
            and self.minz <= round(g.me.z)
            and self.maxz >= round(g.me.z)
        )

    def check(self):
        if self.force_paused:
            return
        r = self.is_in_range()
        if r and not self.inrange:
            self.inrange = True
            self.loop.play_looped()
        elif not r and self.inrange:
            self.inrange = False
            self.loop.pause()

    def __del__(self):
        self.loop.close()


g.sources = []
g.ambs = []


def sourcecheckloop():
    for i in range(len(g.sources)):
        src = g.sources[i]
        # Lazy-init: load audio when player walks close enough
        if not src._audio_ready:
            dist = get_3d_distance(src.lx, src.miny, src.minz, g.me.x, g.me.y, g.me.z)
            if dist <= _LAZY_INIT_DIST:
                src._load_audio()
            continue
        try: g.sources[i].source_sound.handle.volume=g.sources[i].volume
        except: pass
        if g.sources[i].paused != g.sources[i].p2:
            if (
                g.sources[i].paused
                and get_3d_distance(
                    g.sources[i].lx,
                    g.sources[i].miny,
                    g.sources[i].minz,
                    g.me.x,
                    g.me.y,
                    g.me.z,
                )
                > 30
            ):
                g.p.pause_sound(g.sources[i].source_sound)
            elif g.sources[i].paused:
                g.sources[i].paused = False
                g.p.resume_sound(g.sources[i].source_sound)

            if (
                g.sources[i].paused
                and get_3d_distance(
                    g.sources[i].rx,
                    g.sources[i].maxy,
                    g.sources[i].maxz,
                    g.me.x,
                    g.me.y,
                    g.me.z,
                )
                > 30
            ):
                g.p.pause_sound(g.sources[i].source_sound)
            elif g.sources[i].paused:
                g.sources[i].paused = False
                g.p.resume_sound(g.sources[i].source_sound)
        g.sources[i].p2 = g.sources[i].paused
    for i in range(len(g.ambs)):
        g.ambs[i].check()


def destroy_all_sources():
    for i in range(len(g.sources)):
        if g.sources[i]._audio_ready and g.sources[i].source_sound is not None:
            g.p.destroy_sound(g.sources[i].source_sound)
    g.sources.clear()
    g.ambs.clear()


def pause_all_sources():
    for i in range(len(g.sources)):
        g.sources[i].paused = True
    for i in range(len(g.ambs)):
        g.ambs[i].force_paused = True

        g.ambs[i].loop.pause()


def resume_all_sources():
    for i in range(len(g.sources)):
        g.sources[i].paused = False
    for i in range(len(g.ambs)):
        g.ambs[i].force_paused = False
        g.ambs[i].check()


def spawn_source(
    source_lx,
    source_rx,
    source_miny,
    source_maxy,
    source_minz,
    source_maxz,
    soundfile,
    paused=False,
    id=-1, volume=0
):
    source1 = source(
        source_lx,
        source_rx,
        source_miny,
        source_maxy,
        source_minz,
        source_maxz,
        soundfile,
        paused,
        id, volume
    )
    g.sources.append(source1)


def destroy_source(id):
    for i in range(len(g.sources)):
        if g.sources[i].id == id and id > -1:
            if g.sources[i]._audio_ready and g.sources[i].source_sound is not None:
                g.p.destroy_sound(g.sources[i].source_sound)
            g.sources.pop(i)


def create_amb(minx, maxx, miny, maxy, minz, maxz, sound, volume):
    amb1 = amb(minx, maxx, miny, maxy, minz, maxz, sound, volume)
    g.ambs.append(amb1)
