import sound, sound_positioning, traceback
import globals as g
class SoundPoolItem:
    def __init__(self, **kwargs):
        self.handle = sound.sound()
        self.filename = kwargs.get("filename", "")
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.z = kwargs.get("z", 0)
        self.rotation = kwargs.get("rotation", 0)
        self.looping = kwargs.get("looping", 0)
        self.pan_step = kwargs.get("pan_step", 3)
        self.volume_step = kwargs.get("volume_step", 3)
        self.behind_pitch_decrease = kwargs.get("behind_pitch_decrease", 5)
        self.start_pan = kwargs.get("start_pan", 0)
        self.start_volume = kwargs.get("start_volume", 0)
        self.start_pitch = kwargs.get("start_pitch", 0)
        self.start_offset = kwargs.get("start_offset", 0)
        self.upper_range = kwargs.get("upper_range", 0)
        self.lower_range = kwargs.get("lower_range", 0)
        self.left_range = kwargs.get("left_range", 0)
        self.right_range = kwargs.get("right_range", 0)
        self.backward_range = kwargs.get("backward_range", 0)
        self.forward_range = kwargs.get("forward_range", 0)
        self.looping = kwargs.get("looping", False)
        self.is_3d = kwargs.get("is_3d", False)
        self.stationary = kwargs.get("stationary", False)
        self.persistent = kwargs.get("persistent", False)
        self.paused = kwargs.get("paused", False)

    def reset(self):
        self.handle.close()
        self.__init__()

    def update(self, listener_x, listener_y, listener_z, rotation, max_distance):
        if self.handle is not None and self.handle.player is not None:
            self.handle.player.max_distance = max_distance
            if max_distance == 2000:
                self.handle.player.rolloff = 0.05
            else:
                self.handle.player.rolloff = 1.0
        if max_distance > 0 and self.looping:
            total_distance = self.get_total_distance(listener_x, listener_y, listener_z)

            if total_distance > max_distance and self.handle.player != None:
                self.handle.close()
                return
            if total_distance <= max_distance and self.handle.player == None:
                try:
                    self.handle.load(
                        self.filename, False, isinstance(self.filename, bytes)
                    )
                    # Logic fix, no looping or crashing of any sort will occur anymore.
                    if not self.handle.source or not self.handle.player:
                        self.__init__()
                        return
                    self.handle.player.alhrtf=self.alhrtf
                except:
                    traceback.print_exc()
                self.update_listener_position(
                    listener_x, listener_y, listener_z, rotation
                )
                if not self.paused:
                    self.handle.play_looped()
                return
        self.update_listener_position(listener_x, listener_y, listener_z, rotation)

    def update_listener_position(self, listener_x, listener_y, listener_z, rotation):
        if self.handle.player == None:
            return
        if self.stationary:
            return
        delta_left = self.x - self.left_range
        delta_right = self.x + self.right_range
        delta_backward = self.y - self.backward_range
        delta_forward = self.y + self.forward_range
        delta_upper = self.z + self.upper_range
        delta_lower = self.z - self.lower_range
        True_x = listener_x
        True_y = listener_y
        True_z = listener_z

        if not self.is_3d:
            if listener_x >= delta_left and listener_x <= delta_right:
                sound_positioning.position_sound_custom_3d(
                    self.handle,
                    listener_x,
                    0,
                    0,
                    listener_x,
                    2,
                    0,
                    0.0,
                    self.pan_step,
                    self.volume_step,
                    self.behind_pitch_decrease,
                    self.start_pan,
                    self.start_volume,
                    self.start_pitch,
                    False,
                )
                return
            if listener_x < delta_left:
                sound_positioning.position_sound_custom_3d(
                    self.handle,
                    listener_x,
                    0,
                    0,
                    delta_left,
                    2,
                    0,
                    0.0,
                    self.pan_step,
                    self.volume_step,
                    self.behind_pitch_decrease,
                    self.start_pan,
                    self.start_volume,
                    self.start_pitch,
                    False,
                )
            if listener_x > delta_right:
                sound_positioning.position_sound_custom_3d(
                    self.handle,
                    listener_x,
                    0,
                    0,
                    delta_right,
                    2,
                    0,
                    0.0,
                    self.pan_step,
                    self.volume_step,
                    self.behind_pitch_decrease,
                    self.start_pan,
                    self.start_volume,
                    self.start_pitch,
                    False,
                )
            return

        if listener_x < delta_left:
            True_x = delta_left
        elif listener_x > delta_right:
            True_x = delta_right
        if listener_y < delta_backward:
            True_y = delta_backward
        elif listener_y > delta_forward:
            True_y = delta_forward
        if listener_z < delta_lower:
            True_z = delta_lower
        elif listener_z > delta_upper:
            True_z = delta_upper
        sound_positioning.position_sound_custom_3d(
            self.handle,
            listener_x,
            listener_y,
            listener_z,
            True_x,
            True_y,
            True_z,
            rotation,
            self.pan_step,
            self.volume_step,
            self.behind_pitch_decrease,
            self.start_pan,
            self.start_volume,
            self.start_pitch,
            False,
        )
        # Raycast occlusion check in absolute world coordinates
        try:
            # Check if listener or source has moved significantly since last check
            last_l = getattr(self, "_last_occlusion_listener", None)
            last_s = getattr(self, "_last_occlusion_source", None)
            current_l = (listener_x, listener_y, listener_z)
            current_s = (True_x, True_y, True_z)
            
            if (last_l is None or last_s is None or
                abs(last_l[0] - current_l[0]) > 0.8 or
                abs(last_l[1] - current_l[1]) > 0.8 or
                abs(last_l[2] - current_l[2]) > 0.8 or
                abs(last_s[0] - current_s[0]) > 0.8 or
                abs(last_s[1] - current_s[1]) > 0.8 or
                abs(last_s[2] - current_s[2]) > 0.8):
                
                occlusion = sound.get_raycast_occlusion(
                    listener_x, listener_y, listener_z,
                    True_x, True_y, True_z
                )
                self._last_occlusion_val = occlusion
                self._last_occlusion_listener = current_l
                self._last_occlusion_source = current_s
            else:
                occlusion = getattr(self, "_last_occlusion_val", 0.0)
                
            self.handle.direct_occlusion = occlusion
            self.handle.reverb_occlusion = occlusion
        except Exception:
            pass

    def get_total_distance(self, listener_x, listener_y, listener_z):
        if self.stationary:
            return 0
        delta_left = self.x - self.left_range
        delta_right = self.x + self.right_range
        delta_backward = self.y - self.backward_range
        delta_forward = self.y + self.forward_range
        delta_lower = self.z - self.lower_range
        delta_upper = self.z + self.upper_range
        True_x = listener_x
        True_y = listener_y
        True_z = listener_z
        distance = 0
        if not self.is_3d:
            if listener_x >= delta_left and listener_x <= delta_right:
                return distance
            if listener_x < delta_left:
                distance = delta_left - listener_x
            if listener_x > delta_right:
                distance = listener_x - delta_right
            return distance
        if listener_x < delta_left:
            True_x = delta_left
        elif listener_x > delta_right:
            True_x = delta_right
        if listener_y < delta_backward:
            True_y = delta_backward
        elif listener_y > delta_forward:
            True_y = delta_forward
        if listener_z < delta_lower:
            True_z = delta_lower
        elif listener_z > delta_upper:
            True_z = delta_upper
        if listener_x < True_x:
            distance = True_x - listener_x
        if listener_x > True_x:
            distance = listener_x - True_x
        if listener_y < True_y:
            distance += True_y - listener_y
        if listener_y > True_y:
            distance += listener_y - True_y
        if listener_z < True_z:
            distance += True_z - listener_z
        if listener_z > True_z:
            distance += listener_z - True_z
        return distance


class SoundPool:
    def __init__(
        self, max_distance=50, pan_step=20.0, volume_step=2.0, behind_pitch_decrease=5.0
    ):
        self.max_distance = max_distance
        self.pan_step = pan_step
        self.volume_step = volume_step
        self.behind_pitch_decrease = behind_pitch_decrease
        self.items = []
        self.last_listener_x = 0
        self.last_listener_y = 0
        self.last_listener_z = 0
        self.last_rotation = 0
        self.clean_frequency = 8

    def play_stationary(self, filename, looping=False, persistent=False):
        return self.play_stationary_extended(
            filename, looping, 0, 0, 0, 100, persistent
        )

    def play_stationary_extended(
        self,
        filename,
        looping,
        offset,
        start_pan,
        start_volume,
        start_pitch,
        memory=False,
        persistent=False,
    ):
        self.clean_frequency -= 1
        if self.clean_frequency <= 0 and not isinstance(filename, bytes):
            self.clean_unused()
        s = SoundPoolItem(
            filename=filename,
            looping=looping,
            start_offset=offset,
            start_pan=start_pan,
            start_volume=start_volume,
            start_pitch=start_pitch,
            persistent=persistent,
            stationary=True,
        )
        try:
            s.handle.load(filename, False, isinstance(filename, bytes))
            if not s.handle.player or not s.handle.source:
                s.reset()
                return -1
        except:
            s.reset()
            return -1
        if s.start_offset > 0:
            s.handle.position = s.start_offset
        if start_pan != 0.0:
            s.handle.pan = start_pan
        if start_volume < 0.0:
            s.handle.volume = start_volume
        s.handle.pitch = start_pitch
        listener_x=g.me.x
        listener_y=g.me.y
        listener_z=g.me.z
        sound_x=listener_x
        sound_y=listener_y
        sound_z=listener_z
        s.handle.player.stationary=True
        if looping == True:
            s.handle.play_looped()
        else:
            s.handle.play()
        self.items.append(s)
        return s

    def play_1d(self, filename, listener_x, sound_x, looping, persistent=False):
        return self.play_extended_1d(
            filename, listener_x, sound_x, 0, 0, looping, 0, 0, 0, 100, persistent
        )

    def play_extended_1d(
        self,
        filename,
        listener_x,
        sound_x,
        left_range,
        right_range,
        looping,
        offset,
        start_pan,
        start_volume,
        start_pitch,
        persistent=False,
    ):
        self.clean_frequency -= 1
        if self.clean_frequency <= 0:
            self.clean_unused()
        s = SoundPoolItem(
            filename=filename,
            x=sound_x,
            looping=looping,
            stationary=True,
            start_pan=start_pan,
            start_volume=start_volume,
            start_pitch=start_pitch,
            persistent=persistent,
            pan_step=self.pan_step,
            volume_step=self.volume_step,
            behind_pitch_decrease=0.0,
            left_range=left_range,
            right_range=right_range,
            backward_range=0,
            forward_range=0,
            is_3d=False,
            start_offset=offset,
        )
        if (
            self.max_distance > 0
            and s.get_total_distance(listener_x, 0, 0) > self.max_distance
        ):
            if not looping:
                s.reset()
                return -2
            else:
                self.last_listener_x = listener_x
                s.handle.pitch = start_pitch
                s.update(self.listener_x, 0, 0, 0, self.max_distance)
                self.items.append(s)
                return s
        try:
            s.handle.load(filename, False, isinstance(filename, bytes))
            if not s.handle.player or not s.handle.source:
                s.reset()
                return -1

        except:
            s.reset()
            return -1
        if s.start_offset > 0:
            s.handle.position = s.start_offset
        s.handle.pitch = start_pitch
        self.last_listener_x = listener_x
        s.update(listener_x, 0, 0, 0, self.max_distance)
        if looping:
            s.handle.play_looped()
        else:
            s.handle.play()
        self.items.append(s)
        return s

    def play_2d(
        self,
        filename,
        listener_x,
        listener_y,
        sound_x,
        sound_y,
        looping,
        persistent=False,
    ):
        return self.play_extended_2d(
            filename,
            listener_x,
            listener_y,
            sound_x,
            sound_y,
            0,
            0,
            0,
            0,
            looping,
            0,
            0,
            0,
            100,
            persistent,
        )

    def play_extended_2d(
        self,
        filename,
        listener_x,
        listener_y,
        sound_x,
        sound_y,
        left_range,
        right_range,
        backward_range,
        forward_range,
        looping,
        offset,
        start_pan,
        start_volume,
        start_pitch,
        persistent=False,
    ):
        self.clean_frequency -= 1
        if self.clean_frequency <= 0:
            self.clean_unused()
        s = SoundPoolItem(
            filename=filename,
            x=sound_x,
            y=sound_y,
            looping=looping,
            start_pan=start_pan,
            start_volume=start_volume,
            start_pitch=start_pitch,
            persistent=persistent,
            pan_step=self.pan_step,
            volume_step=self.volume_step,
            behind_pitch_decrease=self.behind_pitch_decrease,
            left_range=left_range,
            right_range=right_range,
            backward_range=backward_range,
            forward_range=forward_range,
            is_3d=True,
            start_offset=offset,
        )
        if (
            self.max_distance > 0
            and s.get_total_distance(listener_x, listener_y, 0) > self.max_distance
        ):
            if looping == False:
                s.reset()
                return -2
            else:
                self.last_listener_x = listener_x
                self.last_listener_y = listener_y
                s.update(listener_x, listener_y, 0, 0, self.max_distance)
                self.items.append(s)
                return s
        try:
            s.handle.load(filename, False, isinstance(self.filename, bytes))
            if not s.handle.player or not s.handle.source:
                s.reset()
                return -1

        except:
            s.reset()
            return -1
        if s.start_offset > 0:
            s.handle.position = s.start_offset
        self.last_listener_x = listener_x
        self.last_listener_y = listener_y
        s.update(listener_x, listener_y, 0, 0, self.max_distance)
        if looping:
            s.handle.play_looped()
        else:
            s.handle.play()
        self.items.append(s)
        return s

    def play_3d(
        self,
        filename,
        listener_x,
        listener_y,
        listener_z,
        sound_x,
        sound_y,
        sound_z,
        rotation=0,
        looping=False,
        persistent=False, alhrtf=False
    ):
        return self.play_extended_3d(
            filename,
            listener_x,
            listener_y,
            listener_z,
            sound_x,
            sound_y,
            sound_z,
            rotation,
            0,
            0,
            0,
            0,
            0,
            0,
            looping,
            0,
            0,
            0,
            100,
            persistent, alhrtf
        )

    def play_extended_3d(
        self,
        filename,
        listener_x,
        listener_y,
        listener_z,
        sound_x,
        sound_y,
        sound_z,
        rotation,
        left_range,
        right_range,
        backward_range,
        forward_range,
        upper_range,
        lower_range,
        looping,
        offset,
        start_pan,
        start_volume,
        start_pitch,
        persistent, alhrtf=False
    ):
        if "whiz" not in filename: alhrtf=False
        listener_z+=g.aim
        self.clean_frequency -= 1
        if self.clean_frequency <= 0:
            self.clean_unused()
        s = SoundPoolItem(
            filename=filename,
            x=sound_x,
            y=sound_y,
            z=sound_z,
            rotation=rotation,
            looping=looping,
            pan_step=self.pan_step,
            volume_step=self.volume_step,
            behind_pitch_decrease=self.behind_pitch_decrease,
            start_pan=start_pan,
            start_volume=start_volume,
            start_pitch=start_pitch,
            left_range=left_range,
            right_range=right_range,
            backward_range=backward_range,
            forward_range=forward_range,
            lower_range=lower_range,
            upper_range=upper_range,
            is_3d=True,
            persistent=persistent,
            start_offset=offset,
        )
        if (
            self.max_distance > 0
            and s.get_total_distance(listener_x, listener_y, listener_z)
            > self.max_distance
        ):
            if looping == False:
                s.reset()
                return -2
            else:
                self.last_listener_x = listener_x
                self.last_listener_y = listener_y
                self.last_listener_z = listener_z
                self.last_rotation = rotation
                s.alhrtf=alhrtf
                s.update(
                    listener_x, listener_y, listener_z, rotation, self.max_distance
                )
                self.items.append(s)
                return s
        if 1 == 1:
            s.handle.load(
                filename,
                False
                if listener_x == sound_x
                and listener_y == sound_y
                and listener_z == sound_z
                else True,
                isinstance(filename, bytes),
            )
        else:
            s.reset()
            return -1
        if s.start_offset > 0:
            s.handle.position = s.start_offset
        self.last_listener_x = listener_x
        self.last_listener_y = listener_y
        self.last_listener_z = listener_z
        s.alhrtf=alhrtf
        if s.handle.player is not None: s.handle.player.alhrtf=alhrtf
        s.update(listener_x, listener_y, listener_z, rotation, self.max_distance)

        if looping:
            s.handle.play_looped()
        else:
            s.handle.play()

        self.items.append(s)
        return s

    def sound_is_active(self, s):
        if isinstance(s,int): return False
        if s.handle == None or s.handle.player == None:
            return False
        if not s.handle.player.playing():
            return False
        return True

    def sound_is_playing(self, s):
        if not self.sound_is_active(s):
            return False
        return s.handle.player.playing()

    def pause_sound(self, s):
        if 1 == 1:
            if not self.sound_is_active(s):
                return False
            if s.paused:
                return False
            s.paused = True
            if s.handle.player.playing():
                s.handle.stop()
            return True

    def resume_sound(self, s):
        if 1 == 1:
            if not s.paused:
                return False
            s.paused = False
            if (
                self.max_distance > 0
                and s.get_total_distance(
                    self.last_listener_x, self.last_listener_y, self.last_listener_z
                )
                > self.max_distance
            ):
                if s.handle != None:
                    s.handle.close()
                return True
            s.update(
                self.last_listener_x,
                self.last_listener_y,
                self.last_listener_z,
                self.last_rotation,
                self.max_distance,
            )
            if s.handle != None and not s.handle.player.playing():
                if s.looping:
                    s.handle.play_looped()
                else:
                    s.handle.play()
            return True

    def pause_all(self):
        for i in self.items:
            if self.sound_is_playing(i):
                self.pause_sound(i)

    def resume_all(self):
        for i in self.items:
            if i.handle.player != None:
                self.resume_sound(i)

    def destroy_all(self):
        for i in self.items:
            i.reset()

    def update_listener_1d(self, listener_x):
        self.update_listener_3d(listener_x, 0, 0, 0)

    def update_listener_2d(self, listener_x, listener_y):
        self.update_listener_3d(listener_x, listener_y, 0, 0)

    def update_listener_3d(self, listener_x, listener_y, listener_z, rotation):
        # Dynamic FMOD Reverb Update
        try:
            from map import get_reverb_at
            import fmod_audio
            import sound
            
            r = get_reverb_at(listener_x, listener_y, listener_z)
            props = fmod_audio.system.get_reverb_properties(0)
            if r is not None:
                props.DecayTime = int(r._decay_time * 1000)
                props.Density = float(r._density * 100)
                props.Diffusion = float(r._diffusion * 100)
                props.EarlyDelay = float(r._reflections_delay * 1000)
                props.LateDelay = float(r._late_reverb_delay * 1000)
                props.WetLevel = float(sound._to_db_volume(r._gain))
            else:
                props.WetLevel = -80.0 # Bypass reverb outside reverb zones
            fmod_audio.system.set_reverb_properties(0, props)
        except Exception:
            pass

        # Dynamic FMOD Echo Zone Update
        try:
            from map import get_echo_at
            import fmod_audio
            import sound
            if fmod_audio.initialized and fmod_audio.echo_dsp is not None:
                echo = get_echo_at(listener_x, listener_y, listener_z)
                if echo is not None:
                    fmod_audio.echo_dsp.bypass = False
                    fmod_audio.echo_dsp.set_parameter_float(0, float(echo._delay * 1000.0))
                    fmod_audio.echo_dsp.set_parameter_float(1, float(echo._feedback * 100.0))
                    # Map the initial echo reflection volume (WetLevel) dynamically in dB based on feedback depth
                    wet_vol = float(sound._to_db_volume(echo._feedback))
                    fmod_audio.echo_dsp.set_parameter_float(3, wet_vol)
                else:
                    fmod_audio.echo_dsp.bypass = True
        except Exception:
            pass

        # Dynamic FMOD Water Immersion Lowpass Filter Update
        try:
            from map import get_tile_at
            import fmod_audio
            if fmod_audio.initialized and fmod_audio.lowpass_dsp is not None:
                tile = get_tile_at(listener_x, listener_y, listener_z)
                if tile and "water" in tile.lower():
                    fmod_audio.lowpass_dsp.bypass = False
                    fmod_audio.lowpass_dsp.set_parameter_float(0, 1200.0) # Muffle cutoff frequency at 1.2 kHz
                else:
                    fmod_audio.lowpass_dsp.bypass = True
        except Exception:
            pass

        listener_z+=g.aim
        if len(self.items) == 0:
            return
        self.last_listener_x = listener_x
        self.last_listener_y = listener_y
        self.last_listener_z = listener_z
        self.last_rotation = rotation
        for i in self.items:
            i.update(listener_x, listener_y, listener_z, rotation, self.max_distance)

    def update_sound_1d(self, s, x):
        return self.update_sound_3d(s, x, 0, 0)

    def update_sound_2d(self, s, x, y):
        return self.update_sound_3d(s, x, y, 0)

    def update_sound_3d(self, s, x, y, z):
        try:
            s.x = x
            s.y = y
            s.z = z
            s.update(
                self.last_listener_x,
                self.last_listener_y,
                self.last_listener_z,
                self.last_rotation,
                self.max_distance,
            )
            return True
        except:
            return False

    def update_sound_start_values(self, s, start_pan, start_volume, start_pitch):
        s.start_pan = start_pan
        s.start_volume = start_volume
        s.start_pitch = start_pitch

        s.update(
            self.last_listener_x,
            self.last_listener_y,
            self.last_listener_z,
            self.last_rotation,self.max_distance,
        )
        if s.stationary and s.handle != None:
            s.handle.pan = start_pan
            s.handle.volume = start_volume
            s.handle.pitch = start_pitch
            return True
        if s.is_3d == False and s.handle.pitch != start_pitch:
            s.handle.pitch = start_pitch
        return True

    def update_sound_range_1d(self, s, left_range, right_range):
        return self.update_sound_range_3d(s, left_range, right_range, 0, 0, 0, 0, 0)

    def update_sound_range_2d(
        self, s, left_range, right_range, backward_range, forward_range, rotation
    ):
        return self.update_sound_range_3d(
            s, left_range, right_range, backward_range, forward_range, 0, 0, rotation
        )

    def update_sound_range_3d(
        self,
        s,
        left_range,
        right_range,
        backward_range,
        forward_range,
        lower_range,
        upper_range,
        rotation,
    ):
        s.left_range = left_range
        s.right_range = right_range
        s.backward_range = backward_range
        s.forward_range = forward_range
        s.lower_range = lower_range
        s.upper_range = upper_range
        s.update(
            self.last_listener_x,
            self.last_listener_y,
            self.last_listener_z,
            rotation,
            self.max_distance,
        )
        return True

    def destroy_sound(self, s):
        try:
            s.reset()
            return True
        except:
            return False

    def clean_unused(self):
        if len(self.items) == 0:
            return
        for i in list(self.items):
            if not i.looping and (i.handle == None or i.handle.player==None or not (i.handle.player is not None and (i.handle.player.playing()))) and not i.paused:
                try:
                    if i.handle.player is not None:
                        if not i.handle.player.playing(): i.handle.close()
                    self.items.remove(i)
                except:
                    pass
                self.clean_frequency = 8
