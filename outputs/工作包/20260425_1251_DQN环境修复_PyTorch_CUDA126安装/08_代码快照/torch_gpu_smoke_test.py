from __future__ import annotations

import sys

import torch


def main() -> None:
    print("python", sys.executable)
    print("torch", torch.__version__)
    print("torch cuda", torch.version.cuda)
    print("cuda available", torch.cuda.is_available())
    print("device count", torch.cuda.device_count())

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("device", device)
    if torch.cuda.is_available():
        print("gpu", torch.cuda.get_device_name(0))
    else:
        print("gpu", "NO CUDA")

    torch.manual_seed(20260425)
    model = torch.nn.Sequential(
        torch.nn.Linear(16, 32),
        torch.nn.ReLU(),
        torch.nn.Linear(32, 4),
    ).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)

    x = torch.randn(128, 16, device=device)
    y = torch.randn(128, 4, device=device)

    loss_value = None
    for step in range(10):
        opt.zero_grad(set_to_none=True)
        pred = model(x)
        loss = torch.nn.functional.mse_loss(pred, y)
        loss.backward()
        opt.step()
        loss_value = float(loss.detach().cpu())
        print(f"step={step + 1} loss={loss_value:.8f}")

    if device.type == "cuda":
        torch.cuda.synchronize()
    print("smoke_test", "PASS")


if __name__ == "__main__":
    main()
