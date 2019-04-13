from torch.utils.data import Dataset
import cv2


def load_img(img_path):
    img = cv2.imread(str(img_path))
    if img is None:
        raise FileNotFoundError(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


class ImagesDataset(Dataset):
    def __init__(self, df, image_paths_name, labels_names, is_train, transform):
        df = df[df["is_train"] == int(is_train)]
        self.image_paths = df[image_paths_name].values
        self.transform = transform
        self.labels = df[labels_names].values

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_orig = load_img(self.image_paths[idx])
        image = image_orig
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)

        return image, label.squeeze()
