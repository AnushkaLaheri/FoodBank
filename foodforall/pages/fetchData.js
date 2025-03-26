import { useEffect, useState } from 'react';

const FetchData = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        fetch('http://127.0.0.1:5001/get-foodforall-data')
            .then(response => response.json())
            .then(data => {
                setData(data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, []);

    return (
        <div>
            <h1>Fetched Data</h1>
            <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
    );
};

export default FetchData;