import pygame

class timer:
    """A simple timer class like bgt."""

    def __init__(self):
        self.paused = False
        self.pausedElapsed = 0
        self._forced = None  # forced elapsed time in ms, or None
        self.restart()

    def restart(self):
        """Restarts this timer."""
        self._forced = None
        self.pausedElapsed = 0
        self.startTick = pygame.time.get_ticks()

    @property
    def elapsed(self):
        """
        Returns the elapsed time in milliseconds.

        :rtype: int
        """
        if self._forced is not None:
            if self.paused:
                return self._forced
            else:
                return self._forced + pygame.time.get_ticks() - self._forcedTick
        if self.paused:
            return self.pausedElapsed
        return self.pausedElapsed + pygame.time.get_ticks() - self.startTick

    def setPaused(self, p):
        if p == self.paused:
            return
        if p:
            self.pausedElapsed = self.elapsed
        else:
            if self._forced is not None:
                self._forcedTick = pygame.time.get_ticks()
            else:
                self.startTick = pygame.time.get_ticks()
        self.paused = p

    def force(self, ms):
        """
        Force the timer to act like 'ms' milliseconds have elapsed.
        :param ms: milliseconds
        """
        self._forced = ms
        self._forcedTick = pygame.time.get_ticks()
