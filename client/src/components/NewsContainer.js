import React, { Component } from 'react';
import News from './News';
import NewsData from '../../../server/out/news';


class NewsContainer extends Component {
  renderNews() {
    return NewsData.reverse().map(data =>
      <News key={data.title} news={data} />
    );
  }

  render() {
    const { containerStyle } = styles;

    return (
      <div style={containerStyle}>
        {this.renderNews()}
      </div>
    );
  }
}

const styles = {
  containerStyle: {
    justifyContent: 'center'
  }
};

export default NewsContainer;
