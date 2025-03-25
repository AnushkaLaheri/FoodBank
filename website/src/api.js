import axios from 'axios';

const API_URL = 'http://127.0.0.1:5001';  // Flask backend URL

// Function to get all users
export const getAllUsers = async () => {
    try {
        const response = await axios.get(`${API_URL}/get-all-users`);
        return response.data;
    } catch (error) {
        console.error('Error fetching users:', error);
        return [];
    }
};

// Function to insert food data
export const insertFood = async (foodData) => {
    try {
        const response = await axios.post(`${API_URL}/insert-food`, { mlJson: foodData });
        return response.data;
    } catch (error) {
        console.error('Error inserting food:', error);
        return { message: "Error occurred" };
    }
};
