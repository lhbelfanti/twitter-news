import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCalendarAlt } from '@fortawesome/free-solid-svg-icons';

const Date = ({ date }) => {
  const { containerStyle, itemStyle } = styles;
  return (
    <div style={containerStyle}>
      <FontAwesomeIcon style={itemStyle} icon={faCalendarAlt} />
      <div style={itemStyle} >Publicado el {date}</div>
    </div>
  );
};

const styles = {
  containerStyle: {
    fontSize: 14,
    display: 'flex',
    marginBottom: 20,
    flexDirection: 'row',
    color: '#999',
    justifyContent: 'flex-start',
  },
  itemStyle: {
    marginRight: 5
  }
};

export { Date };