import logging
import os
import time
from logging.handlers import RotatingFileHandler

try:
	import psutil
except Exception:
	psutil = None


LOG_DIR = os.environ.get("ZHA_LOG_DIR", "logs")
SUMMARY_INTERVAL_MS = int(os.environ.get("ZHA_PERF_LOG_INTERVAL_MS", "5000"))
SPIKE_THRESHOLD_MS = float(os.environ.get("ZHA_PERF_SPIKE_MS", "12"))


def _ensure_log_dir():
	try:
		os.makedirs(LOG_DIR, exist_ok=True)
	except Exception:
		pass


def get_logger(name, filename=None):
	_ensure_log_dir()
	logger = logging.getLogger("zha." + name)
	if logger.handlers:
		return logger
	logger.setLevel(logging.INFO)
	logger.propagate = False
	logfile = os.path.join(LOG_DIR, filename or (name + ".log"))
	handler = RotatingFileHandler(logfile, maxBytes=2 * 1024 * 1024, backupCount=5, encoding="utf-8")
	handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
	logger.addHandler(handler)
	return logger


class PerformanceMonitor:
	def __init__(self):
		self.logger = get_logger("performance", "performance.log")
		self.interval_start = time.perf_counter()
		self.loop_count = 0
		self.loop_total_ms = 0.0
		self.net_total_ms = 0.0
		self.game_total_ms = 0.0
		self.max_loop_ms = 0.0
		self.max_net_ms = 0.0
		self.max_game_ms = 0.0
		self.spike_count = 0
		self.process = psutil.Process(os.getpid()) if psutil else None
		if self.process:
			try:
				self.process.cpu_percent(None)
			except Exception:
				self.process = None
		self.logger.info("performance monitor started spike_threshold_ms=%s summary_interval_ms=%s", SPIKE_THRESHOLD_MS, SUMMARY_INTERVAL_MS)

	def sample(self, loop_ms, net_ms, game_ms, globals_module=None):
		self.loop_count += 1
		self.loop_total_ms += loop_ms
		self.net_total_ms += net_ms
		self.game_total_ms += game_ms
		self.max_loop_ms = max(self.max_loop_ms, loop_ms)
		self.max_net_ms = max(self.max_net_ms, net_ms)
		self.max_game_ms = max(self.max_game_ms, game_ms)

		if loop_ms >= SPIKE_THRESHOLD_MS:
			self.spike_count += 1
			self.logger.warning(
				"tick spike loop_ms=%.3f net_ms=%.3f game_ms=%.3f players=%s zombies=%s npcs=%s transits=%s",
				loop_ms,
				net_ms,
				game_ms,
				self._count(globals_module, "players"),
				self._count(globals_module, "zombies"),
				self._count(globals_module, "npcs"),
				self._count(globals_module, "transits"),
			)

		elapsed_ms = (time.perf_counter() - self.interval_start) * 1000.0
		if elapsed_ms >= SUMMARY_INTERVAL_MS:
			self._write_summary(elapsed_ms, globals_module)
			self._reset_interval()

	def _write_summary(self, elapsed_ms, globals_module):
		if self.loop_count <= 0:
			return
		avg_loop = self.loop_total_ms / self.loop_count
		avg_net = self.net_total_ms / self.loop_count
		avg_game = self.game_total_ms / self.loop_count
		cpu = self._cpu_percent()
		mem_mb = self._memory_mb()
		net_stats = self._network_stats(globals_module)
		self.logger.info(
			"summary interval_ms=%.0f ticks=%s avg_loop_ms=%.3f max_loop_ms=%.3f avg_net_ms=%.3f max_net_ms=%.3f avg_game_ms=%.3f max_game_ms=%.3f spikes=%s players=%s zombies=%s npcs=%s items=%s chests=%s transits=%s cpu_percent=%s rss_mb=%s %s",
			elapsed_ms,
			self.loop_count,
			avg_loop,
			self.max_loop_ms,
			avg_net,
			self.max_net_ms,
			avg_game,
			self.max_game_ms,
			self.spike_count,
			self._count(globals_module, "players"),
			self._count(globals_module, "zombies"),
			self._count(globals_module, "npcs"),
			self._count(globals_module, "items"),
			self._count(globals_module, "chests"),
			self._count(globals_module, "transits"),
			cpu,
			mem_mb,
			net_stats,
		)

	def _reset_interval(self):
		self.interval_start = time.perf_counter()
		self.loop_count = 0
		self.loop_total_ms = 0.0
		self.net_total_ms = 0.0
		self.game_total_ms = 0.0
		self.max_loop_ms = 0.0
		self.max_net_ms = 0.0
		self.max_game_ms = 0.0
		self.spike_count = 0

	def _count(self, globals_module, name):
		try:
			return len(getattr(globals_module, name))
		except Exception:
			return 0

	def _cpu_percent(self):
		if not self.process:
			return "n/a"
		try:
			return round(self.process.cpu_percent(None), 2)
		except Exception:
			return "n/a"

	def _memory_mb(self):
		if not self.process:
			return "n/a"
		try:
			return round(self.process.memory_info().rss / (1024 * 1024), 2)
		except Exception:
			return "n/a"

	def _network_stats(self, globals_module):
		try:
			n = globals_module.n
			return "enet_recv_bytes={} enet_recv_packets={} enet_sent_bytes={} enet_sent_packets={}".format(
				n.get_total_received_data(),
				n.get_total_received_packets(),
				n.get_total_sent_data(),
				n.get_total_sent_packets(),
			)
		except Exception:
			return "enet_stats=n/a"
