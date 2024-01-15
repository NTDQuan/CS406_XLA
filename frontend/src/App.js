import React, { useState } from 'react';
import './App.css';
import InputBar from './components/InputBar.js'
import ImageSelector from './components/ImageSelector.js';
import ImageDisplay from './components/ImageDisplay.js';
import TransformButton from './components/TransformButton.js'

function App() {
    const [selectedImage, setSelectedImage] = useState(null);
    const [object, setObject] = useState('');
    const [newObject, setNewObject] = useState('');
    const [resultImage, setResultImage] = useState(null);
    return (
        
        <div className="App">
            <ImageDisplay selectedImage={selectedImage} resultImage={resultImage}/>
            <ImageSelector setSelectedImage={setSelectedImage}/>
            <InputBar setObject={setObject} setNewObject={setNewObject}/>
            <TransformButton object={object} newObject={newObject} selectedImage={selectedImage} setResultImage={setResultImage} />
        </div>
    );
}

export default App;