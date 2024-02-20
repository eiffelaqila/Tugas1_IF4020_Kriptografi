import React, { useState } from "react";
import axios from "axios";
import { FaLock, FaUnlock, FaDownload } from "react-icons/fa"

function App() {
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  const [data, setData] = useState({
    inputType: "text",
    function: "vigenere",
  })
  const [cipherType, setCipherType] = useState('');

  const [isLoading, setLoading] = useState(false);
  const [result, setResult] = useState(undefined);
  const [fileResult, setFileResult] = useState(undefined);
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

  const handleDownloadResult = (e) => {
    const url = URL.createObjectURL(fileResult);

    const a = document.createElement("a");
    a.href = url;
    a.download = fileResult.name;

    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    URL.revokeObjectURL(url);
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

    setResult(undefined);
    setFileResult(undefined);
    setLoading(true);
    
    const mappedData = mapDataToAxiosValue(data);
    const cipherType = e.nativeEvent.submitter.value;
    setCipherType(cipherType);
    
    try {
      if (data.inputType === "text") {
        const response = await axios.post(
          `${backendUrl}/${data.function}/${cipherType}`,
          mappedData
        )

        const fileResponse = new File(
          [response.data],
          "result",
          {
            type: 'text/plain',
          },
        )

        setLoading(false);
        setResult({
          text: response.data,
          base64: btoa(response.data),
        });
        setFileResult(fileResponse);
      } else {
        const file = data.file;
        const formData = new FormData();
        formData.append("file", file);

        if (["vigenereext", "super"].includes(data.function)) {
          const response = await axios.post(
            `${backendUrl}/${data.function}/${cipherType}-file`,
            formData,
            {
              params: { ...mappedData },
              responseType: 'arraybuffer'
            },
          );
  
          const binaryData = new Uint8Array(response.data);

          const fileResponse = new File(
            [binaryData],
            file ? `${cipherType}ed-${file.name}` : `${cipherType}ed-result`,
            {
              type: file ? file.type : 'text/plain',
            },
          )

          setLoading(false);
          setResult({
            base64: "Too large to display.",
          });
          setFileResult(fileResponse);

          return;
        }

        const response = await axios.post(
          `${backendUrl}/${data.function}/${cipherType}-file`,
          formData,
          {
            params: { ...mappedData },
          },
        );

        const fileResponse = new File(
          [response.data],
          file ? `${cipherType}ed-${file.name}` : `${cipherType}ed-result`,
          {
            type: file ? file.type : 'text/plain',
          },
        )

        setLoading(false);
        setResult({
          text: response.data,
          base64: btoa(response.data),
        });
        setFileResult(fileResponse);
      }

      setLoading(false);
      setError(undefined);
    } catch (e) {
      setLoading(false);
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
              <input type="file" id="file" placeholder="Enter file" onChange={(e) => handleChangeFile(e)} required={data.inputType === "file"} />
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
        <hr className="h-px my-8 bg-gray-700 border-0" />
        <div className={`items-center justify-center w-full ${isLoading ? "flex" : "hidden"}`}>
            <svg aria-hidden="true" className="w-8 h-8 text-gray-200 animate-spin fill-indigo-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#e5e7eb"/>
                <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
            </svg>
            <span className="sr-only">Loading...</span>
        </div>
        {error && (
          <div className="w-full py-2 my-4">
            <div className="w-full p-4 mt-4 bg-red-100 border border-red-300 rounded-md">
              <h2 className="text-xl font-bold text-gray-700">Error</h2>
              <p>{JSON.stringify(error.message)}</p>
            </div>
          </div>
        )}
        {result && (
          <div className="w-full py-2 my-4">
            <h2 className="text-xl font-bold text-gray-700">{cipherType === 'encrypt' ? 'Encrypted' : 'Decrypted'} Text</h2>
            <div className="w-full my-4">
              <div className="w-full my-4">
                <h5 className="text-sm font-semibold text-gray-800">Base64 Result</h5>
                <div className="w-full p-4 overflow-x-scroll border border-gray-300 rounded-md max-h-lg bg-gray-50">
                  <p className="text-base font-medium text-gray-800">{result.base64}</p>
                </div>
              </div>
              <div className={`w-full my-4 ${result.text ? "block" : "hidden"}`}>
                <h5 className="text-sm font-semibold text-gray-800">Text Result</h5>
                <div className="w-full p-4 overflow-x-scroll border border-gray-300 rounded-md max-h-lg bg-gray-50">
                  <p className="text-base font-medium text-gray-800">{result.text}</p>
                </div>
              </div>
            </div>
            <button type="button" onClick={(e) => handleDownloadResult(e)} className="bg-indigo-700 hover:bg-indigo-600 focus:bg-indigo-600">
              <FaDownload /> Download File
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
