import React from "react";

const KeywordCloudView = () => {
  return (
    <div>
      <h3>Keyword Clouds</h3>

      <img
        src="http://localhost:5000/graphs/sample_keyword_cloud.png"
        alt="Keyword Cloud"
        style={{ width: "100%", maxWidth: "800px" }}
      />
    </div>
  );
};

export default KeywordCloudView;
