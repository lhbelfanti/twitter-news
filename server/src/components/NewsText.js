import React from 'react';
import InformationModal from './InformationModal';

const NewsText = ({ data }) => {
  const { text } = data;
  const { containerStyle } = styles;
  return (
    <div style={containerStyle}>
      <p>{text}</p>
      <InformationModal data={data} />
    </div>
  );
};

const styles = {
  containerStyle: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'flex-start',
  }
};

export default NewsText;
