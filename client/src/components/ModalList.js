import React, { Component } from 'react';
import ModalListItem from './ModalListItem';

class ModalList extends Component {
  state = { index: 0 };

  constructor(props) {
    super(props);
    this.noticeElement = React.createRef();
    this.imagesElement = React.createRef();
    this.linksElement = React.createRef();
    this.hashtagsElement = React.createRef();
    this.mentionsElement = React.createRef();
    this.cashtagsElement = React.createRef();

    this.options = [
        this.noticeElement,
        this.imagesElement,
        this.linksElement,
        this.hashtagsElement,
        this.mentionsElement,
        this.cashtagsElement];
  }

  onMenuClicked(id) {
    this.options.forEach((option) => {
      option.current.className = 'item';
    });

    this.options[id].current.className = 'item active';

    this.setState({ index: id });
  }

  render() {
    const { containerStyle, menuStyle } = styles;

    return (
        <div style={containerStyle}>
            <div className="ui vertical fluid tabular menu" style={menuStyle}>
              <a
                className="item active"
                ref={this.noticeElement}
                onClick={() => { this.onMenuClicked(0); }}
              >
                Noticia
              </a>
              <a
                className="item"
                ref={this.imagesElement}
                onClick={() => { this.onMenuClicked(1); }}
              >
                Imágenes
              </a>
              <a
                className="item"
                ref={this.linksElement}
                onClick={() => { this.onMenuClicked(2); }}
              >
                Links
              </a>
              <a
                className="item"
                ref={this.hashtagsElement}
                onClick={() => { this.onMenuClicked(3); }}
              >
                Hashtags
              </a>
              <a
                className="item"
                ref={this.mentionsElement}
                onClick={() => { this.onMenuClicked(4); }}
              >
                Mentions
              </a>
              <a
                className="item"
                ref={this.cashtagsElement}
                onClick={() => { this.onMenuClicked(5); }}
              >
                Cashtags
              </a>
            </div>
          <ModalListItem index={this.state.index} data={this.props.data} />
        </div>
    );
  }
}

const styles = {
    containerStyle: {
      display: 'flex',
      flexDirection: 'row'
    },
    menuStyle: {
      flexBasis: '30%',
      marginRight: 10
    }
};

export default ModalList;