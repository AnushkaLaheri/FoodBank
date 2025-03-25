import React from 'react';

function ListFood(props) {
    const data = props.data;

    // Checking if the data object is valid and contains required properties
    if (!data || !data.item || !data.donation_score) {
        return <p>Loading...</p>;  // Show loading or error message if data is missing
    }

    return (
        <div className="food-recognition">
            <p>
                <strong>Our model recognized your object as a(n)</strong> {data.item}.
                <br />
                <strong>Donating this item will grant you</strong> {data.donation_score} points!
            </p>
        </div>
    );
}

export default ListFood;
