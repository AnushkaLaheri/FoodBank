import React from 'react'

function ListFood(props) {
    const data = props.data
    console.log("data: ", data)
    return (
        <div>
            <p>
                Our model recognized your object as a(n) {data["item"]}.
                <br></br>
                Donating this item will grant you {data["donation_score"]} points!
            </p>
        </div>
    )
}

export default ListFood
