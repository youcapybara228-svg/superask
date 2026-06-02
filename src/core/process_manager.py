import asyncio
from enum import Enum
from dataclasses import dataclass


class SAState(Enum):
    OFF = "off"
    ON = "on"
    SESSION_OFF = "offc"
    PERMANENTLY_OFF = "offall"


@dataclass
class ProcessManager:
    state: SAState = SAState.OFF
    active_task: asyncio.Task | None = None

    @property
    def is_running(self) -> bool:
        return self.state == SAState.ON

    def start(self):
        self.state = SAState.ON

    def stop(self):
        self.state = SAState.OFF
        self.stop_active()

    def stop_session(self):
        self.state = SAState.SESSION_OFF
        self.stop_active()

    def disable_permanently(self):
        self.state = SAState.PERMANENTLY_OFF
        self.stop_active()

    def stop_active(self):
        if self.active_task and not self.active_task.done():
            self.active_task.cancel()
            self.active_task = None

    def can_run(self) -> bool:
        return self.state == SAState.ON


process_manager = ProcessManager()
