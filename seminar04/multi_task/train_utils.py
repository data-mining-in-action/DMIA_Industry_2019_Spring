import torch
import time

class Metric:
    def __init__(self, name):
        self.name = name
    def __call__(self, outputs, targets):
        pass


def train(train_loader, model, criterion, optimizer, epoch, args, metrics):
    batch_time = AverageMeter("Batch time")
    data_time = AverageMeter("Data time")
    losses = AverageMeter("Loss")
    avg_meters = []
    for m in metrics:
        avg_meters.append(AverageMeter(name=m.name))
    # switch to train mode
    model.train()

    end = time.time()
    for i, (input, target) in enumerate(train_loader):
        # measure data loading time
        data_time.update(time.time() - end)

        input = input.to(args.device)
        target = target.to(args.device)

        # compute output
        output = model(input)
        loss = criterion(output, target)

        # measure accuracy and record loss
        with torch.no_grad():
            losses.update(loss.item(), input.size(0))
            for j in range(len(metrics)):
                avg_meters[j].update(metrics[j](output, target), input.size(0))

        # compute gradient and do SGD step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        if i % args.print_freq == 0:
            message = 'Epoch: [{0}][{1}/{2}]\t' \
                      'Loss {losses.val:.4f} ({losses.avg:.4f})\t'.format(
                       epoch, i, len(train_loader), batch_time=batch_time,
                       data_time=data_time, losses=losses)
            for meter in avg_meters:
                message += f"{meter.name} {meter.val:.4f} ({meter.avg:.4f})\t"

            print(message)


def validate(val_loader, model, criterion, args, metrics):
    batch_time = AverageMeter("Batch time")
    losses = AverageMeter("Loss")
    avg_meters = []
    for m in metrics:
        avg_meters.append(AverageMeter(name=m.name))
    # switch to evaluate mode
    model.eval()
    with torch.no_grad():
        end = time.time()
        for i, (input, target) in enumerate(val_loader):
            input = input.to(args.device)
            target = target.to(args.device)

            # compute output
            output = model(input)
            loss = criterion(output, target)

            # measure accuracy and record loss
            losses.update(loss.item(), input.size(0))
            for j in range(len(metrics)):
                avg_meters[j].update(metrics[j](output, target), input.size(0))

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            if i % args.print_freq == 0:

                message = 'Test: [{0}/{1}]\t' \
                          'Loss {loss.val:.4f} ({loss.avg:.4f}) \t'.format(
                    i, len(val_loader), batch_time=batch_time, loss=losses)
                for meter in avg_meters:
                    message += f"{meter.name} {meter.val:.4f} ({meter.avg:.4f})\t"

                print(message)

        message = ' * Loss {losses.avg:.3f}\t'.format(losses=losses)
        for meter in avg_meters:
            message += f"{meter.name} {meter.avg:.4f}\t"
        print(message)

    return


class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self, name):
        self.reset()
        self.name = name

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


class AccuracyMetric(Metric):
    def __init__(self):
        super().__init__(name="Acc")

    def __call__(self, output, targets):
        return accuracy(output, targets)


class AccuracyPart(Metric):
    def __init__(self, name, output_slice, target_column):
        super().__init__(name)
        self.output_slice = output_slice
        self.target_column = target_column

    def __call__(self, output, targets):
        return accuracy(output[:, self.output_slice], targets[:, self.target_column])


import torch.nn as nn


class L1Part(Metric):
    def __init__(self, name, output_column, target_column):
        super().__init__(name)
        self.output_column = output_column
        self.target_column = target_column

    def __call__(self, output, targets):
        return nn.L1Loss(output[:, self.output_column], targets[:, self.target_column])


def accuracy(output, target):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        batch_size = target.size(0)
        _, pred = torch.max(output, dim=1)
        correct = pred.eq(target).float()
        return correct.sum().mul_(100.0 / batch_size).item()
