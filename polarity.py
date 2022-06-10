import typing
from typing import Any, Optional, Text, Dict, List, Type

from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.constants import TEXT
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message
from rasa.nlu.tokenizers import whitespace_tokenizer

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata

from nltk.classify import NaiveBayesClassifier

import pickle
import os

SENTIMENT_MODEL_FILE_NAME = "sentiment_classifier.pkl"

class SentimentAnalyzer(Component):
    """A sentiment analysis component"""

    # Which components are required by this component.
    # Listed components should appear before the component itself in the pipeline.
    @classmethod
    def required_components(cls) -> List[Type[Component]]:
        """Specify which components need to be present in the pipeline."""

        return [whitespace_tokenizer.WhitespaceTokenizer]

    defaults = {}
    supported_language_list = ['es']
    not_supported_language_list = None

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None, clf=None) -> None:
        super(SentimentAnalyzer, self).__init__(component_config=component_config)
        self.clf = clf

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Train this component."""

        training_data = training_data.training_examples #list of Message objects
        tokens = []
        labels = []
        for example in training_data:
            if 'text_tokens' in example.data:
                if example.get('metadata')['example']['sentiment'] is not None:
                    labels.append(example.get('metadata')['example']['sentiment'])
                    tokens.append([t.text for t in example.data['text_tokens']])

        processed_tokens = [self.preprocessing(t) for t in tokens]
        labeled_data = [(t, x) for t,x in zip(processed_tokens, labels)]
        self.clf = NaiveBayesClassifier.train(labeled_data)

    def preprocessing(self, tokens):
        """Create bag-of-words representation of the training examples."""
        
        return({word: True for word in tokens})

    def convert_to_rasa(self, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""

        entity = {
            "value" : value,
            "confidence" : confidence,
            "entity" : "sentiment",
            "extractor" : "sentiment_extractor"
        }

        return entity

    def process(self, message: Message, **kwargs: Any) -> None:
        """Process an incoming message."""

        if not self.clf:
            # component is either not trained or didn't receive enough training data
            entity = None
        else:
            if 'text_tokens' in message.data:
                tokens= [t.text for t in message.data['text_tokens']]
                tb = self.preprocessing(tokens=tokens)
                pred = self.clf.prob_classify(tb)
                sentiment = pred.max()
                confidence = pred.prob(sentiment)
                entity = self.convert_to_rasa(value=sentiment, confidence=confidence)
                message.set("entities", [entity], add_to_output=True)
            else:
                entity = None

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""

        if self.clf:
            model_file_name = os.path.join(model_dir, SENTIMENT_MODEL_FILE_NAME)
            self._write_model(model_file_name, self.clf)
            return {"classifier_model" : SENTIMENT_MODEL_FILE_NAME}

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Text,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any,
    ) -> "Component":
        """Load this component from file."""

        file_name = meta.get('classifier_model')
        classifier_file = os.path.join(model_dir, file_name)

        if os.path.exists(classifier_file):
            classifier_f = open(classifier_file, 'rb')
            clf = pickle.load(classifier_f)
            classifier_f.close()
            return cls(meta, clf)
        else:
            return cls(meta)

    def _write_model(self, model_file, classifier) -> None:
        """Helper to save and load model properly"""

        save_classifier = open(model_file, 'wb')
        pickle.dump(classifier, save_classifier)
        save_classifier.close()