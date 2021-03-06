from quicktext.imports import *
from quicktext.data.classifier_data import TextClassifierData


class Trainer:
    """
    This class is used to train the models in quicktext
    """

    def __init__(self, classifier):
        """
        Constructor function for Trainer class
        Args:
            classifier (TextClassifier): Text classifier class
            train (list): List of tuples of form (text, label) for training
            val (list): List of tuples of form  (text, label) for validation
            test (list): List of tuples of form  (text, label) for test
        Returns:   
            None
        """

        self.classifier = classifier

    def load_data(self, data, batch_size):
        """
        This function takes data to return 
        a torch dataloader
        Args:
            data (list): list of tuples
        Returns:
            torch DataLoader:  Torch dataloader
        """

        dataset = TextClassifierData(self.classifier.vocab, data)
        loader = DataLoader(
            dataset, batch_size=batch_size, collate_fn=dataset.get_batch
        )
        return loader

    def fit(self, train, val, epochs=1, batch_size=32, gpu=False):
        """
        This function trains the model
        Args:
            epochs (int): Number of epoch to train the model
            gpus (int): Number of GPUs to use
        Return:
            None
        """

        train_loader = self.load_data(train, batch_size)
        val_loader = self.load_data(val, batch_size)

        if gpu is False:
            ngpus = 0
        else:
            ngpus = 1

        trainer = pl.Trainer(max_epochs=epochs, gpus=ngpus)
        trainer.fit(self.classifier.model, train_loader, val_loader)

    def test(self, test, batch_size=32, gpu=False, ngpus=0):
        """
        This function tests model using test set
        Args:
            gpus (int): The number of gpus
        Returns:
            None
        """

        if gpu is False:
            ngpus = 0
        else:
            ngpus = ngpus

        test_loader = self.load_data(test, batch_size)

        trainer = pl.Trainer(gpus=ngpus)
        trainer.test(self.classifier.model, test_dataloaders=test_loader)
