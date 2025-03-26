import { useState } from 'react';

const SendData = () => {
    const [response, setResponse] = useState(null);

    const sendData = () => {
        const dataToSend = {
            key: 'value' // Replace with your actual data
        };

        fetch('http://127.0.0.1:5001/send-foodforall-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend)
        })
            .then(response => response.json())
            .then(data => {
                setResponse(data);
            })
            .catch(error => {
                console.error('Error sending data:', error);
            });
    };

    return (
        <div>
            <h1>Send Data</h1>
            <button onClick={sendData}>Send Data</button>
            <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
    );
};

export default SendData;