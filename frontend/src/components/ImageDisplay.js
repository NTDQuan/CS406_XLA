import React, { useEffect, useState } from "react";
import '../style/ImageDisplay.css'

const ImageDisplay = ( {selectedImage, resultImage} ) => {
    const [inputImage, setInputImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(false);

    useEffect(() => {
        setLoading(true);
        setInputImage(selectedImage);
        setLoading(false);
    }, [selectedImage]);

    useEffect(() => {
        setResult(resultImage)
    }, [resultImage]);

    return (
        <div className="ImageContainer">
            {loading && <div className="spinner"></div>}
            <div className="InputImage">
                {inputImage ? (
                        <img
                            alt=""
                            src={URL.createObjectURL(inputImage)}
                            onLoad={() => setLoading(false)}
                        />
                    ) : (
                        <p>No image selected</p>
                    )}
            </div>
            <div className="OutputImage">
                {result instanceof Blob ? (
                            <img
                                alt=""
                                src={URL.createObjectURL(result)}
                                onLoad={() => setLoading(false)}
                            />
                        ) : (
                            <p></p>
                        )}

            </div>
        </div>
    )
}

export default ImageDisplay;