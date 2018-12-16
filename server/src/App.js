import React, { Component } from 'react';

import './styles/App.css';
import NewsContainer from './components/NewsContainer';


class App extends Component {
  render() {
    return (
      <div>
        <h1>Twitter News</h1>
        <NewsContainer />
      </div>
    );
  }
}

export default App;
