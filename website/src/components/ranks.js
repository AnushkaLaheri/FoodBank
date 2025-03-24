import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card, Image } from 'react-bootstrap';
import { FaHome } from 'react-icons/fa';
import './ranks.css';

const Ranks = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await fetch('http://localhost:5001/get-all-users');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                const formattedData = data.map(user => ({
                    id: user[0],
                    username: user[1],
                    points: user[2]
                }));
                const sortedData = formattedData.sort((a, b) => b.points - a.points);
                setUsers(sortedData);
            } catch (error) {
                console.error('Error fetching user data:', error);
            }
        };

        fetchUsers();
    }, []);

    const sortedUsers = users.sort((a, b) => b.points - a.points);

    return (
        <div className='bodytypeshit'>
            <div >        
                <h1 className="text-warning">Leaderboard</h1>
                <div className='top-5' style={{ position: 'relative', padding: '20px', left: "2vw" }}>
                    {/* Home Icon on the Left */}
                    <a href="/" style={{ textDecoration: 'none', color: 'black', position: 'absolute', top: '10px', left: '10px' }}>
                        <FaHome size={40} className="fg-warning text-warning" /> {/* Adjust size if needed */}
                    </a>
                </div>
                <br>
                </br>
                <div className='table-of-stuff'>
                    <table>
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Name</th>
                                <th>Points</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sortedUsers.map((user, index) => (
                                <tr key={user.id}>
                                    <td>{index + 1}</td>
                                    <td>{user.username}</td>
                                    <td>{user.points}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Ranks;
