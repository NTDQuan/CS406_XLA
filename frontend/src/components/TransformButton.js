import React, { useState, useEffect } from "react";
import Button from '@mui/material/Button';
import sendRequest from "../services/SendRequest";

const TransformButton = ({ object, newObject, selectedImage, setResultImage }) => {
    const [loading, setLoading] = useState(false);

    const handleSendRequest = async () => {
        setLoading(true);
        console.log("Form Data:", {
            object,
            newObject,
            selectedImage
        });

        try {
            const resultBlob = await sendRequest(object, newObject, selectedImage);
            setResultImage(resultBlob);
            console.log("Request successful");
        } catch (error) {
            console.error("Request failed:", error.message);
        } finally {
            setLoading(false); // Set loading state back to false whether the request succeeds or fails
        }
    };

    return (
        <Button onClick={handleSendRequest} variant="contained" disabled={loading}>
            {loading ? "Loading..." : "Transform"}
        </Button>
    )
}

export default TransformButton