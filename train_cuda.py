import numpy as np
import torch

def mini_batch_train(data_loader, model, optimizer, loss_fn, device):
    mini_batch_losses = []
    for x_batch, y_batch in data_loader:
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)
        # 置为训练状态
        model.train()
        # Step 1 - 前向计算预测值
        yhat = model(x_batch)
        # Step 2 - 计算损失
        mini_batch_loss = loss_fn(yhat, y_batch)
        # Step 3 - 计算梯度
        mini_batch_loss.backward()
        # Step 4 - 参数更新
        optimizer.step()
        optimizer.zero_grad()

        mini_batch_losses.append(mini_batch_loss.detach().cpu().item())

    loss = np.mean(mini_batch_losses)
    return loss


def mini_batch_val(data_loader, model, loss_fn, device):
    mini_batch_losses = []
    for x_batch, y_batch in data_loader:
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)
        # 置为验证状态
        model.eval()
        # Step 1 - 前向计算预测值
        yhat = model(x_batch)
        # Step 2 - 计算损失
        mini_batch_loss = loss_fn(yhat, y_batch)
        mini_batch_losses.append(mini_batch_loss.detach().cpu().item())

    loss = np.mean(mini_batch_losses)
    return loss


def train(model, train_loader, test_loader, loss_fn, 
          optimizer, epochs, device):
    # 指定随机数种子，可以再现数据
    np.random.seed(23)
    torch.manual_seed(23)

    # 循环轮数计数
    losses = []  # 每轮训练的损失
    val_losses = []  #  每轮验证数据的损失

    for total_epochs, _ in enumerate(range(epochs)):
        model.train()

        # 进入mini-batch的内循环
        loss = mini_batch_train(train_loader, model, optimizer, loss_fn, device)
        losses.append(loss)

        if test_loader:
        # 验证数据集（验证不需要计算梯度）
            with torch.inference_mode():
                # 验证集的 mini_batch
                val_loss = mini_batch_val(test_loader, model, loss_fn, device)
                val_losses.append(val_loss)

        if test_loader:
            print(
                f"Epoch {total_epochs + 1}/{epochs} - loss: {loss:.4f} - val_loss: {val_losses[-1]:.4f}"
            )
        else:
            print(
                f"Epoch {total_epochs + 1}/{epochs} - loss: {loss:.4f}"
            )

    return losses, val_losses
