import React from 'react';

const Title = ({ text }) => {
  const { containerStyle, textStyle } = styles;

  return (
    <div style={containerStyle}>
      <h2 style={textStyle}>
        {text}
      </h2>
    </div>
  );
};

const styles = {
  containerStyle: {
    alignItems: 'flex-start'
  },
  textStyle: {
    display: 'block',
    marginTop: 0,
    marginBottom: 5,
  }
};

export { Title };
