const BASE_URL = "http://127.0.0.1:8000";

const sendRequest = async (object, newObject, image) => {
    try {
        const formData = new FormData();
        formData.append("object", object);
        formData.append("newObject", newObject);
        formData.append("selectedImage", image);

        const response = await fetch(`${BASE_URL}/upload`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.text();
            console.error("Error response from server:", errorData);
            throw new Error("Request failed");
        }

        const resultBlob = await response.blob(); // or use response.arrayBuffer()

        return resultBlob;
    } catch (error) {
        console.error("Error sending request: ", error.message)
        throw error;
    }
}

export default sendRequest;