import React, { useState } from "react";

const ImageSelector = ({setSelectedImage}) => {
    const onImageChange = Event => {
        console.log(Event.target.files[0]);
        setSelectedImage(Event.target.files[0]);
    }

    return (
        <input
            type="file"
            name="inputImage"
            onChange={onImageChange}
        />
    )
}

export default ImageSelector