import React, { useState } from "react";

function App() {
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  const [data, setData] = useState({
    inputType: "text",
    function: "vigenere",
  })

  const [output, setOutput] = useState(undefined);

  const mapDataToAxiosValue = (d) => {
    let data = {
      inputType: d.inputType,
      function: d.function,
      key: d.key,
      cipherType: d.cipherType,
    }
  
    if (data.inputType === "text") {
      return ({
        ...data,
        inputText: d.inputText,
      })
    }
    
    return ({
      ...data,
      file: d.file,
    })
  }

  const handleChange = (e) => {
    let newData = {...data};
    newData[e.target.id] = e.target.value;

    console.log(`Setting new value: ${e.target.value} for ${e.target.id}`)
    setData(newData);
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    const cipherType = e.nativeEvent.submitter.value;

    console.log(`Pressed button: ${cipherType}`)
    setOutput(mapDataToAxiosValue({
      ...data,
      cipherType,
    }));
  }

  const showIfType = (type) => data.inputType === type ? "" : "hidden";

  return (
    <div className="relative flex flex-col justify-center min-h-screen bg-white">
      <div className="w-full p-6 m-auto lg:max-w-xl">
        <h1 className="text-3xl font-bold">Classic Cipher</h1>
        <div className="w-full py-2 m-auto">
          <form onSubmit={(e) => handleSubmit(e)} className="flex flex-col gap-2 mt-6">
            <div>
              <label htmlFor="inputType">Input Type</label>
              <select id="inputType" defaultValue="text" onChange={(e) => handleChange(e)}>
                <option value="text">Text</option>
                <option value="file">File</option>
              </select>
            </div>
            <div className={showIfType("text")}>
              <label htmlFor="inputText">Plaintext / Ciphertext</label>
              <input type="text" id="inputText" placeholder="Enter text" onChange={(e) => handleChange(e)} required={data.inputType === "text"} />
            </div>
            <div className={showIfType("file")}>
              <label htmlFor="file">File</label>
              <input type="file" id="file" placeholder="Enter file" onChange={(e) => handleChange(e)} required={data.inputType === "file"} />
            </div>
            <div>
              <label htmlFor="function">Cipher Function</label>
              <select id="function" defaultValue="vigenere" onChange={(e) => handleChange(e)}>
                <option value="vigenere">Vigenere Cipher</option>
                <option value="vigenereauto">Auto-Key Vigenere Cipher</option>
                <option value="vigenereext">Extended Vigenere Cipher</option>
                <option value="playfair">Playfair Cipher</option>
                <option value="affine">Affine Cipher</option>
                <option value="hill">Hill Cipher</option>
                <option value="super">Super Enkripsi</option>
              </select>
            </div>
            <div>
              <label htmlFor="key">Key</label>
              <input type="text" id="key" placeholder="Enter key" onChange={(e) => handleChange(e)} required />
            </div>
            <div className="flex gap-2 mt-6">
              <button type="submit" value="encrypt" className="bg-indigo-700 hover:bg-indigo-600 focus:bg-indigo-600">
                Encrypt
              </button>
              <button type="submit" value="decrypt" className="bg-orange-700 hover:bg-orange-600 focus:bg-orange-600">
                Decrypt
              </button>
            </div>
          </form>
        </div>
        {output && (
          <div className="w-full py-2 m-auto">
            <h2 className="text-xl font-semibold">Output</h2>
            <p><strong>Accessing backend url:</strong> {backendUrl}</p>
            <p><strong>Input object:</strong> {JSON.stringify(output, null, 2)}</p>
          </div>
        )}
      </div>      
    </div>
  );
}

export default App;
