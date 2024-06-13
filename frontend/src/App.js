import React, { useState } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Navbar from './Components/NavBar';
import UploadContainer from './UploadContainer';
import RecommendationPage from './Components/recommendations';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('upload');
  const [showPages, setShowPages] = useState(true);

  const handleNextButtonClick = () => {
    setShowPages(false);
  };

  return (
      <div className="App">
        <Navbar />
        {showPages && (<h1 className="header">Upload Your Documents</h1>)}

        {showPages && (
          <div className="upload-section">
            <UploadContainer title="Pension Scheme"/>
            <UploadContainer title="Employee Data" />
            <UploadContainer title="Pricing" />
          </div>
        )}
        {showPages && (
          <button className="submit-button" onClick={handleNextButtonClick}>
            Next
          </button>
        )}
        {!showPages && (
            <RecommendationPage />
        )}
      </div>
  );
}

export default App;
