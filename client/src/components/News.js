import React from 'react';
import { Title, Date, Picture } from './common';
import NewsText from './NewsText';

const News = ({ news }) => {
  const { title, creation_date, images } = news;
  const image = images[Math.floor(Math.random() * images.length)];

  const { itemStyle, bodyContainerStyle} = styles;

  return (
    <div style={itemStyle}>
      <div>
        <Title text={title} />
        <Date date={creation_date} />
      </div>
      <div style={bodyContainerStyle}>
        <Picture src={image} alt={title} />
        <NewsText data={news} />
      </div>
    </div>
  );
};

const styles = {
  itemStyle: {
    width: 800,
    height: 350,
    margin: 'auto',
    borderRadius: 10,
    borderWidth: 1,
    borderStyle: 'solid',
    borderColor: '#d7d7d7',
    padding: 20,
    marginBottom: 20,
  },
  bodyContainerStyle: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'flex-start',
  }
};

export default News;
