import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card, Image } from 'react-bootstrap';
import './Profile.css';
import { FaHome } from 'react-icons/fa';


import profile from '../assets/profile.png';

function UserProfile() {
  const [submittedItems, setSubmittedItems] = useState([]);
  const userId = 1
  const [username, setUsername] = useState(''); // State for username

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        // Fetch user data
        const response = await fetch(`http://localhost:5001/get-user-data/${userId}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();

        const formattedData = data.map(item => ({
          name: item[0],
          date: item[1],
          points: item[2],
        }));

        setSubmittedItems(formattedData);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };

    const fetchUsername = async () => {
      try {
        const response = await fetch(`http://localhost:5001/get-username/${userId}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setUsername(data[0]); // Set the username state
      } catch (error) {
        console.error('Error fetching username:', error);
      }
    };

    fetchUserData();
    fetchUsername(); // Call to fetch the username
  }, [userId]);

  return (
    <div style={{ backgroundColor: '#79745C', minHeight: '100vh' }}>
      <div
        style={{
          backgroundColor: '#709176',
          backgroundPosition: 'center',
          height: '15rem',
        }}
        className="bg-cover bg-center h-250 position-relative"
      >
        <Container fluid>
          <Row className="justify-content-center align-items-center" style={{ height: '100%' }}>
            <Col md={1} className="text-center">
              {/* Home Icon on the Left */}
              <a href="/" style={{ textDecoration: 'none', color: 'white' }}>
                <FaHome size={40} /> {/* Adjust the size as needed */}
              </a>
            </Col>
            
            <Col md={2} className="text-center">
              <Image
                src={profile}
                roundedCircle
                style={{ width: '27vh', border: '5px solid white', position: 'relative', top: '10rem' }}
                className="rounded-circle"
              />
            </Col>
            <Col md={7} className="text-center text-white mt-5">
              <div className="name-div">
                <h1 className="mt-3">{username || 'Loading...'}</h1> {/* Display username */}
              </div>
            </Col>
            <Col md={3} className="text-center text-white mt-5">
              <div className="leaderboard-status">
              </div>
            </Col>
          </Row>
        </Container>
      </div>

      {/* History Section */}
      <Container className="mt-5 pt-lg-0 pt-4">
        <h2 className="mb-4 m-md-5">History of Submitted Items</h2>
        <Row>
          {submittedItems.map((item, index) => (
            <Col md={6} lg={4} key={index} className="mb-4">
              <Card>
                <Card.Body>
                  <Card.Title>{item.name}</Card.Title>
                  <Card.Subtitle className="mb-2 text-muted">
                  </Card.Subtitle>
                  <Card.Text>
                    Submitted on: {new Date(item.date).toLocaleString()} <br />
                    Points: {item.points}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </Container>
    </div>
  );
}

export default UserProfile;
