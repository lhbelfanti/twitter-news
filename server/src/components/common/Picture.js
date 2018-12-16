import React from 'react';

const Picture = ({ src, alt }) => {
  const { containerStyle, imageStyle } = styles;

  return (
    <div style={containerStyle}>
      <a href={src}>
        <img
          style={imageStyle}
          src={src}
          alt={alt}
        />
      </a>
    </div>
  );
};

const styles = {
  containerStyle: {
    marginRight: 10
  },
  imageStyle: {
    width: 200,
    height: 200,
    borderRadius: 10,
    borderWidth: 2,
    borderStyle: 'solid',
    borderColor: '#55acee',
  }
};

export { Picture };
