#classifier comparison
#streamlit run app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

#streamlit setup
st.title('Classifier Comparison Tool')

st.write("""
# Evaluate Different Machine Learning Models
Compare classifiers on various datasets and visualize the results.
""")

#dataset sidebar
dataset_options = ['Iris', 'Breast Cancer', 'Wine']
dataset_choice = st.sidebar.selectbox('Choose Dataset', dataset_options)

#classifier sidebar
classifier_options = ['KNN', 'SVM', 'Random Forest']
classifier_choice = st.sidebar.selectbox('Choose Classifier', classifier_options)

def load_data(dataset_name):
    """Load dataset based on user choice."""
    if dataset_name == 'Iris':
        data = datasets.load_iris()
    elif dataset_name == 'Wine':
        data = datasets.load_wine()
    elif dataset_name == 'Breast Cancer':
        data = datasets.load_breast_cancer()
    else:
        st.error("Dataset not available.")
        return None, None
    return data.data, data.target

X, y = load_data(dataset_choice)
if X is None or y is None:
    st.stop()

st.write('Dataset dimensions:', X.shape)
st.write('Class count:', len(np.unique(y)))

def configure_params(classifier):
    """Set parameters based on selected classifier."""
    params = {}
    if classifier == 'SVM':
        C = st.sidebar.slider('Regularization Strength (C)', 0.01, 10.0, 1.0)
        params['C'] = C
    elif classifier == 'KNN':
        neighbors = st.sidebar.slider('Number of Neighbors (K)', 1, 20, 5)
        params['n_neighbors'] = neighbors
    elif classifier == 'Random Forest':
        max_depth = st.sidebar.slider('Max Depth of Trees', 2, 20, 10)
        n_estimators = st.sidebar.slider('Number of Trees', 10, 200, 100)
        params['max_depth'] = max_depth
        params['n_estimators'] = n_estimators
    return params

params = configure_params(classifier_choice)

def create_classifier(classifier, params):
    """Create and return classifier based on user input."""
    if classifier == 'SVM':
        return SVC(C=params['C'])
    elif classifier == 'KNN':
        return KNeighborsClassifier(n_neighbors=params['n_neighbors'])
    elif classifier == 'Random Forest':
        return RandomForestClassifier(n_estimators=params['n_estimators'], max_depth=params['max_depth'], random_state=42)

model = create_classifier(classifier_choice, params)

#splitting data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

try:
    #training model
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    #display accuracy
    accuracy = accuracy_score(y_test, y_pred)
    st.write(f'Chosen Model: {classifier_choice}')
    st.write(f'Accuracy: {accuracy:.2f}')
    
    #display classification report
    st.write("### Detailed Classification Report")
    st.text(classification_report(y_test, y_pred))
    
    #PCA and 2d visualization
    pca = PCA(n_components=2)
    X_reduced = pca.fit_transform(X)
    x1 = X_reduced[:, 0]
    x2 = X_reduced[:, 1]
    
    #plot PCA results
    fig, ax = plt.subplots()
    scatter = ax.scatter(x1, x2, c=y, alpha=0.7, cmap='coolwarm')
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    fig.colorbar(scatter, ax=ax, label='Target Variable')
    
    st.pyplot(fig)
except Exception as e:
    st.error(f"An error occurred during model training or visualization: {e}")
