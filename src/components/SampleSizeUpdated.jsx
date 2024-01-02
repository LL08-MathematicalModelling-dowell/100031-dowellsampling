import React, { useEffect } from 'react'
import ClipLoader from "react-spinners/ClipLoader";
import { Checkbox } from '@mui/material'
import { useState } from 'react'
import "./samplesize.css"
import { Table, TableHead, TableBody, TableRow, TableCell } from '@mui/material';
import Popup from 'reactjs-popup';
const SampleSizeUpdated = () => {
    const [type,setType] = useState("infinite")
    const [sKnown,setSKnown] = useState(false)
    const [standard_deviation,set_standard_deviation]=useState(null)
    const [conf,set_conf]=useState(false)
    const [population_size,set_population_size] = useState(null)
    const [error,setError]=useState(-1)
    const [confidence_level,set_confidence_level]=useState(null)
    const [toggle,setToggle] = useState(false)
    const [buttonClicked,setButtonClicked] = useState(false)
    const [data,setData] = useState({});    
    const [disableButton,setDisableButton] = useState(true)
    const [valueExceedErr,setValueExceedErr] = useState(false)
    const [valueExceedSD,setValueExceedSD] = useState(false)
    const [valueExceedCL,setValueExceedCL] = useState(false)
    const handleSubmit =async () => 
{

var data;
if(error < 0 && error > 1 )
{
  alert("Correct Error Inputs!")
}
else if(standard_deviation < 0 && standard_deviation > 1 )
{
  alert("Correct Standard Deviation Inputs!")
}
// else if(error === -1)
// {
//   setDisableButton(true)
// }
else
{
  setDisableButton(true)
setButtonClicked(true)

if(conf){
 data =
    {
    population_size:type === 'finite' ? parseFloat(population_size) : null ,
    error:parseFloat(error),
    standard_deviation: parseFloat(standard_deviation),
    confidence_level : parseFloat(confidence_level)
    }
  }
  else if(!conf)
  {
    data =
    {
    population_size:type === 'finite' ? parseFloat(population_size) : null ,
    error:parseFloat(error),
    standard_deviation: parseFloat(standard_deviation),
    }
  }
console.log(data)
 fetch("https://100102.pythonanywhere.com/sample-size/", {
  // fetch("http://127.0.0.1:8000/sample-size/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(data),
})

  .then((response) => response.json())
  .then((data) => {
    console.log(data)
    if(data.error)
    
    {
      console.log('This is error ', data.error)
      alert("Check your inputs!")
      // setToggle(false)

    }
    else
    {

      setData(data)
      setToggle(true)
      setButtonClicked(false)
      setDisableButton(false)
    }
    //   console.log(data);
    
  })
  .catch((error) => {
    // Handle any errors that occurred during the request
  });
 
    // }

}
}

const handleError =(e)=>{
  const es = e.target.value
  if(es < 1 && es > 0){ 
    setValueExceedErr(false)
  setError(e.target.value)
  setDisableButton(false)
  }
  else   if(es <= 0 || es >= 1){ 
    setValueExceedErr(true)
    setDisableButton(true)
  }

}
 const handleStandardDeviation=(e)=>{
  const es = e.target.value
  if(es < 1 && es >0){ 
    setValueExceedSD(false)
  set_standard_deviation(e.target.value)
  setDisableButton(false)
  }
  else   if(es <= 0 || es >= 1){ 
  setDisableButton(true)
  setValueExceedSD(true)
  }

 }
 const handleConfidenceLevel =(e)=>{
const es = e.target.value
  if(es <= 100 && es >= 0){ 
    setValueExceedCL(false)
  set_confidence_level(e.target.value)
  setDisableButton(false)
  }
  else   if(es <= 0 || es >= 1){ 
  setDisableButton(true)
  setValueExceedCL(true)
  }

 }
  return (
    <div>
 <div className='mobile'>
 <h3 style={{textAlign:"center",paddingTop:"1em"}}>Sample Size Experiment</h3>
  
            
 <div style={{display:"flex",padding:"1em",justifyContent:"space-between",gap:"1em"}}>
 <div>
 <table  style={{minWidth:"19rem"}}>
  <tr>
    <td>Type</td>
    <td>
            <select className="form-control"
        id="color"
        name="color"
        // value={type}
        onChange={e=>setType(e.target.value)}
      >

        <option disabled>--select--</option>
        <option value="infinite">Infinite</option>
        <option value="finite">Finite</option>
      </select>
    </td>
  </tr>
  {/* {type === 'finite' &&  */}
  <tr>
    <td>Population Size <Popup trigger=
                {<button className='infoButton'>?</button>}
                position="right center" >
                <div style={{width:"50%",background:"white",borderRadius:"1em",padding:"0.5em"}}>The population size refers to the total number of individuals, items, or data points in the entire group or set under study. It is denoted as "N" and is a crucial parameter for sampling methods and calculations.</div>
                
            </Popup></td>
    <td>
      
      <input disabled={type === "infinite"}  className="form-control" placeholder='Enter N'  onChange={e=>set_population_size(e.target.value)} type='number' />
      
    </td>
  </tr>
  {/* } */}
  <tr>
    <td>Error <Popup trigger=
                {<button className='infoButton'>?</button>}
                position="right center" >
                <div style={{width:"50%",background:"white",borderRadius:"1em",padding:"0.5em"}}> Error in statistics represents the difference between an estimated or observed value and the true or actual value. It quantifies the inaccuracy in a measurement or estimation and can be positive (overestimation) or negative (underestimation).</div>
                
            </Popup></td>
    <td>
        
       <input type='number' required min='0' max="1" step=".1" className="form-control" placeholder='Range 0 to 1'  onChange={e=>handleError(e)}/>


    </td>
    {valueExceedErr && <td><p>Range (0 - 1)<span style={{color:"red"}}>*</span></p></td>}
  </tr>
  <tr>
    <td>
    <tr>
      <td>
        Standard Deviation <Popup trigger=
                {<button className='infoButton'>?</button>}
                position="right center" >
                <div style={{width:"50%",background:"white",borderRadius:"1em",padding:"0.5em"}}>The standard deviation is a measure of the spread or variability of data in a dataset. It quantifies how individual data points deviate from the mean (average) of the dataset. A lower standard deviation indicates less variability, while a higher one suggests greater variability.</div>
                
            </Popup>
      </td>
    <td >
     <Checkbox  style={{}} onChange={e=>setSKnown(!sKnown)}/>
    </td>
    </tr>    
    </td>
    <td>       {sKnown && <>   <input min={0} max={1} step=".1" className="form-control" placeholder='Range 0 to 1' onChange={e=>handleStandardDeviation(e)} type='number'/> </>}</td>
  {valueExceedSD && <td><p>Range (0 - 1)<span style={{color:"red"}}>*</span></p></td>}
  </tr>
  
  <tr>

  <td>
  <tr>
    <td>
      Confidence Level <Popup trigger=
                {<button className='infoButton'>?</button>}
                position="right center" >
                <div style={{width:"50%",background:"white",borderRadius:"1em",padding:"0.5em"}}>A confidence interval is a range of values that is calculated from a sample using a formula that incorporates the standard error of the sample mean and a chosen level of confidence. It provides a range within which we can reasonably expect the true population parameter to fall, given the sample data and the chosen confidence level.</div>
                
            </Popup>
    </td>
<td >
   <Checkbox  style={{marginLeft:'0.9em'}} onChange={e=>set_conf(!conf)}/>
</td>
</tr>
  </td>
  <td>
    {
        conf && <>
         <input type='number' required min='0' max="100"  className="form-control" placeholder='Range 0 to 100'  onChange={(e)=>handleConfidenceLevel(e)}/>
       {/* <select className="form-control " onChange={(e)=>set_confidence_level(e.target.value)}>
        <option disabled>--select--</option>
        <option>0.90</option>
        <option>0.95</option>
        <option>0.99</option>
        </select> */}
        </>
        }
  </td>
  {valueExceedCL && <td><p>Range (0 - 100)<span style={{color:"red"}}>*</span></p></td>}
  </tr>
  <tr>
    <button onClick={handleSubmit} className="btn btn-primary" disabled={disableButton} >Submit</button>
  </tr>
  
  
</table>
</div>
<div>
            {!toggle  ? 
<h3 >Response will appear here<span style={{color:"red"}}>*</span></h3>
:
 
<>
                    <h2>Response</h2>
  <Table className="styled-table" style={{maxWidth:"1px"}}>
          <TableHead>
            <TableRow >
              <TableCell style={{fontWeight:"bolder"}}>Sample Size</TableCell>
              <TableCell style={{fontWeight:"bolder"}}>Process Time</TableCell>
              <TableCell style={{fontWeight:"bolder"}}>Method Used</TableCell>
              {/* Add more TableCell elements for additional columns */}
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>{data.sample_size}</TableCell>
              <TableCell>{data.process_time}</TableCell>
              <TableCell>{data.method_used}</TableCell>
            </TableRow>
          </TableBody>
          </Table>
</>
}
        {!toggle && buttonClicked &&
 
     <div style={{marginLeft:"30%",justifyContent:"center"}}> 
      <ClipLoader
        color="green"
        loading={true}
        size={50}
        aria-label="Loading Spinner"
        data-testid="loader"
      />
      </div>
 
 }

    </div>
    </div>
    </div>
  </div>
  )
}

export default SampleSizeUpdated
