import React, { useState } from "react";
import axios from "axios";
import { FaLock, FaUnlock } from "react-icons/fa"

function App() {
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  const [data, setData] = useState({
    inputType: "text",
    function: "vigenere",
  })
  const [cipherType, setCipherType] = useState('');
  const [result, setResult] = useState(undefined);
  const [error, setError] = useState(undefined);

  const mapDataToAxiosValue = (d) => {
    const data = {};
    if (d.inputType === "text") {
      data.inputText = d.inputText;
    }

    if (d.function === "affine") {
      data.keyA = d.keyA;
      data.keyB = d.keyB;
    } else {
      data.key = d.key;
    }
    
    return data;
  }

  const handleChange = (e) => {
    let newData = {...data};
    newData[e.target.id] = e.target.value;
    setData(newData);
  }

  const handleChangeFile = (e) => {
    let newData = {...data};
    newData.file = e.target.files[0];
    setData(newData);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const mappedData = mapDataToAxiosValue(data);
    const cipherType = e.nativeEvent.submitter.value;
    setCipherType(cipherType);
    
    try {
      if (data.inputType === "text") {
        const response = await axios.post(
          `${backendUrl}/${data.function}/${cipherType}`,
          mappedData
        )

        setResult(response.data);
      } else {
        const file = data.file;
        const formData = new FormData();
        formData.append("file", file);

        const response = await axios.post(
          `${backendUrl}/${data.function}/${cipherType}-file`,
          formData,
          {
            params: { ...mappedData },
          },
        );

        const fileResponse = new File(
          [response.data],
          file ? file.name : "result",
          {
            type: file ? file.type : 'text/plain',
          },
        )

        console.log(fileResponse);
        setResult(response.data);
      }

      setError(undefined);
    } catch (e) {
      setError(e);
    }
  }

  const isType = (type) => data.inputType === type;
  const isFunction = (fun) => data.function === fun;

  return (
    <div className="relative flex flex-col justify-center min-h-screen bg-white">
      <div className="w-full px-6 py-10 m-auto lg:max-w-xl">
        <h1 className="text-3xl font-bold text-gray-700">Tugas 1 IF4020 - Kriptografi</h1>
        <h3 className="pt-2 font-medium leading-normal text-gray-500 text-md">
          Oleh:
          <br />
          - 13520074 - Eiffel Aqila Amarendra
          <br />
          - 13520125 - Ikmal Alfaozi
        </h3>
        <div className="w-full py-2 my-4">
          <form onSubmit={(e) => handleSubmit(e)} className="flex flex-col gap-2 mt-6">
            <div>
              <label htmlFor="inputType">Input Type</label>
              <select id="inputType" defaultValue="text" onChange={(e) => handleChange(e)}>
                <option value="text">Text</option>
                <option value="file">File</option>
              </select>
            </div>
            <div className={isType("text") ? "" : "hidden"}>
              <label htmlFor="inputText">Plaintext / Ciphertext</label>
              <input type="text" id="inputText" placeholder="Enter text" onChange={(e) => handleChange(e)} required={data.inputType === "text"} />
            </div>
            <div className={isType("file") ? "" : "hidden"}>
              <label htmlFor="file">File</label>
              <input type="file" id="file" placeholder="Enter file" onChange={(e) => handleChangeFile(e)} required={data.inputType === "file"} accept={data.function !== "vigenereext" ? "text/plain" : undefined} />
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
            <div className={!isFunction('affine')  ? "" : "hidden"}>
              <label htmlFor="key">Key</label>
              <input type="text" id="key" placeholder="Enter key" onChange={(e) => handleChange(e)} required={data.function !== 'affine'} />
            </div>
            <div className={isFunction('affine')  ? "" : "hidden"}>
              <label htmlFor="keyA">Key A (Affine only)</label>
              <input type="text" id="keyA" placeholder="Enter key a" onChange={(e) => handleChange(e)} required={data.function === 'affine'} />
            </div>
            <div className={isFunction('affine')  ? "" : "hidden"}>
              <label htmlFor="keyB">Key B (Affine only)</label>
              <input type="text" id="keyB" placeholder="Enter key b" onChange={(e) => handleChange(e)} required={data.function === 'affine'} />
            </div>
            <div className="flex gap-2 mt-6">
              <button type="submit" value="encrypt" className="bg-indigo-700 hover:bg-indigo-600 focus:bg-indigo-600">
                <FaLock /> Encrypt
              </button>
              <button type="submit" value="decrypt" className="bg-orange-700 hover:bg-orange-600 focus:bg-orange-600">
                <FaUnlock /> Decrypt
              </button>
            </div>
          </form>
        </div>
        {error && (
          <div className="w-full py-2 my-4">
            <div className="w-full p-4 mt-4 bg-red-100 border border-red-300 rounded-md">
              <h2 className="text-xl font-bold text-gray-700">Error</h2>
              <p>{error.message}</p>
            </div>
          </div>
        )}
        {result && (
          <div className="w-full py-2 my-4">
            <h2 className="text-xl font-bold text-gray-700">{cipherType === 'encrypt' ? 'Encrypted' : 'Decrypted'} Text</h2>
            <div className="w-full p-4 mt-4 overflow-x-scroll border border-gray-300 rounded-md bg-gray-50">
              <p>{result}</p>
            </div>
          </div>
        )}
      </div>      
    </div>
  );
}

export default App;
