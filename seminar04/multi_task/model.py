import torch.nn as nn
from torchvision.models import resnet18


class Flatten(nn.Module):
    def forward(self, input):
        return input.view(input.size(0), -1)


class ResnetModel(nn.Module):
    def __init__(self, num_outputs, dp=0.5):
        super().__init__()
        self.num_outputs = num_outputs
        base_model = resnet18(pretrained=True)
        self.features = nn.Sequential(
            base_model.conv1,
            base_model.bn1,
            base_model.relu,
            base_model.maxpool,
            base_model.layer1,
            base_model.layer2,
            base_model.layer3,
            base_model.layer4)
        num_features = base_model.layer4[1].conv1.in_channels
        self.features.requires_grad = False
        self.head = nn.Sequential(
            nn.AdaptiveMaxPool2d(1),
            Flatten(),
            nn.BatchNorm1d(num_features),
            nn.Dropout(p=dp/2),
            nn.Linear(in_features=num_features, out_features=512),
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(512),
            nn.Dropout(p=dp),
            nn.Linear(in_features=512, out_features=self.num_outputs, bias=True)
        )

    def forward(self, input):
        features = self.features(input)
        output = self.head(features)
        return output

    def get_embedding(self, input):
        features = self.features(input)
        embedding = features
        for l in self.head[:-1]:
            embedding = l(embedding)
        return embedding