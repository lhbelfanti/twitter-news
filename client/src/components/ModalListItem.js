import React, { Component } from 'react';
import { Picture } from './common';

class ModalListItem extends Component {
  constructor(props) {
    super(props);

    this.renderText = this.renderText.bind(this);
    this.renderImages = this.renderImages.bind(this);
    this.renderLinks = this.renderLinks.bind(this);
    this.renderHashtags = this.renderHashtags.bind(this);
    this.renderMentions = this.renderMentions.bind(this);
    this.renderCashtags = this.renderCashtags.bind(this);

    this.items = [
      this.renderText,
      this.renderImages,
      this.renderLinks,
      this.renderHashtags,
      this.renderMentions,
      this.renderCashtags
    ];

    this.id = 0;
  }

  renderItem() {
    return this.items[this.props.index]();
  }

  renderText() {
    const { text } = this.props.data;
    return (
      <div>
        <p>{text}</p>
      </div>
    );
  }

  renderImages() {
    const { title, images } = this.props.data;
    return (
      <div style={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap' }}>
        {images.map((image) =>
          <Picture src={image} alt={title} key={this.id++} />
        )}
      </div>
     );
  }

  renderLinks() {
    const { links } = this.props.data;
    return (
      <div key={this.id++}>
        {links.map((link) =>
          <li key={this.id++}>
            <a href={link} key={this.id++}>{link}</a>
          </li>
        )}
      </div>
    );
  }

  renderHashtags() {
    const { hashtags } = this.props.data;
    return (
      <div key={this.id++}>
        {hashtags.map((hashtag) =>
          <li key={this.id++}>
            <a href={`https://twitter.com/hashtag/${hashtag}?src=hash`} key={this.id++}>#{hashtag}</a>
          </li>
        )}
      </div>
    );
  }

  renderMentions() {
    const { mentions } = this.props.data;
    return (
      <div>
        {mentions.map((mention) =>
          <li key={this.id++}>
            <a href={`https://twitter.com/${mention}`} key={this.id++}>@{mention}</a>
          </li>
        )}
      </div>
    );
  }

  renderCashtags() {
    const { cashtags } = this.props.data;
    return (
      <div>
        {cashtags.map((cashtag) =>
          <li key={this.id++}>
            <a href={`https://twitter.com/search?q=%24${cashtag}&src=ctag`} key={this.id++}>${cashtag}</a>
          </li>
        )}
      </div>
    );
  }

  render() {
    return (
      <div>
        {this.renderItem()}
      </div>
    );
  }
}

export default ModalListItem;
