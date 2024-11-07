# language_audio_detection
## Intoduction
The scope of this project encompasses the development of a robust language identification system capable of accurately discerning spoken languages from audio recordings. The primary objective is to leverage machine learning and deep learning techniques to create an efficient and reliable solution that can handle diverse linguistic inputs with high accuracy. Additionally, the project aims to explore augmentation
## Proposed System
The training data included synthetic audio samples created using speech synthesis
techniques and real audio samples from Indian language datasets
Deep Learning-based Approach: Our proposed system leverages the power of deep
learning techniques, specifically Convolutional Neural Networks (CNNs) and Transfer
Learning. By utilizing CNNs for feature extraction and transfer learning with pre-trained
models like VGG16, we aim to capture high-level language features automatically from Mel-spectrogram representations.
Dimensionality Reduction: To address the curse of dimensionality and enhance computational efficiency, we apply Principal Component Analysis (PCA) for feature reduction. This allows us to maintain relevant information while reducing the input dimensionality for classification.
Artificial Neural Network (ANN) Classifier: Our system incorporates an ANN classifier trained on the extracted features to perform language classification. The ANN model learns to map the reduced feature space to language labels, enabling accurate language identification. 
The proposed system offers several advantages over traditional methods, including
Enhanced Accuracy: Deep learning models can learn complex patterns and nuances in language data, leading to improved classification accuracy. The system can adapt to different dialects, accents, and speaking styles, making it robust in diverse linguistic contexts.
Scalability: Deep learning models are highly scalable and can handle large volumes of data efficiently, making them suitable for real-world applications.


<img width="608" alt="pp" src="https://github.com/user-attachments/assets/e2123b9c-30be-43b1-a69b-d74b6c4ff01d">



## Installation 
### Prerequisites
- Python 3.x
- Django
- Other dependencies listed in `requirements.txt` 
### Installation Steps
  ```bash
# Clone the repository
 git clone https://github.com/saron715/language_audio_detection.git
# Navigate to the project directory
cd language_audio_detection
# Install dependencies
 pip install -r requirements.txt
# Apply migrations
 python manage.py migrate
# Run the Django development server
 python manage.py runserver


Hugging face : https://huggingface.co/spaces/saronium/Indian-language-identification-from-audio
