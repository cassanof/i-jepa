
class WarmUpScheduler(object):
    """Copilot wrote this, made some small tweaks though."""
    def __init__(self, 
                 optimizer, 
                 scheduler, 
                 warmup_iter, 
                 total_iter = 300000,
                 min_lr = 1e-6):
        self.optimizer = optimizer
        self.scheduler = scheduler(optimizer, 
                                   total_iter - warmup_iter, 
                                   eta_min = min_lr,)
        self.warmup_iter = warmup_iter
        self.iter = 0
    
    def step(self):
        if self.iter < self.warmup_iter:
            lr = self.iter / self.warmup_iter * self.scheduler.get_last_lr()[0]
            for param_group in self.optimizer.param_groups:
                param_group['lr'] = lr
        else:
            self.scheduler.step()
        self.iter += 1

def losses_to_running_loss(losses, alpha = 0.95):
    running_losses = []
    running_loss = losses[0]
    for loss in losses:
        running_loss = (1 - alpha) * loss + alpha * running_loss
        running_losses.append(running_loss)
    return running_losses
