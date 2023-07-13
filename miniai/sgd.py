# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/12_accel_sgd.ipynb.

# %% auto 0
__all__ = ['BaseSchedulerCB', 'BatchSchedCB', 'RecorderCB', 'EpochSchedulerCB']

# %% ../nbs/12_accel_sgd.ipynb 1
import torch
from .datasets import *
from .conv import *
from .learner import *
from .activations import *
from .init import *

# %% ../nbs/12_accel_sgd.ipynb 49
class BaseSchedulerCB(Callback):
    def __init__(self, sched): self.sched = sched
    def before_fit(self, learn: Learner): self.sched_opt = self.sched(learn.opt)
    def _step(self, learn: Learner): 
        if learn.training:
            self.sched_opt.step()

# %% ../nbs/12_accel_sgd.ipynb 50
class BatchSchedCB(BaseSchedulerCB):
    def after_batch(self, learn): self._step(learn)

# %% ../nbs/12_accel_sgd.ipynb 51
class RecorderCB(Callback):
    def __init__(self, **d): self.d = d
    def before_fit(self, learn: Learner):
        self.recs = {k: [] for k in self.d}
        self.pg = learn.opt.param_groups[0]
        
    def after_batch(self, learn: Learner):
        if not learn.training: return
        for k, v in self.d.items():
            self.recs[k].append(v(self))
            
    def plot(self):
        for k, v in self.recs.items():
            plt.plot(v, label=k)
            plt.legend()
            plt.show()

# %% ../nbs/12_accel_sgd.ipynb 57
class EpochSchedulerCB(BaseSchedulerCB):
    def after_epoch(self, learn: Learner): self._step(learn)
