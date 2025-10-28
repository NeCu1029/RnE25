import torch

for i in range(40):
    f = open(f"models/model{i}.txt", "w")
    model = torch.jit.load(f"models/model{i}.pt")
    model.eval()

    for name, param in model.state_dict().items():
        if param.dim() == 2:
            for i in param:
                for j in i:
                    f.write(f"{round(float(j), 8)} ")
                f.write("\n")
        else:
            for i in param:
                f.write(f"{round(float(i), 8)} ")
            f.write("\n")
        f.write("\n")
    f.close()
