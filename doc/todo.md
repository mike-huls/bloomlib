### Make python wrappers accept iterable
1. Make add_bulk accept any iterable
2. serialization 
3. ~~Upgrade vec<u8> to bitvector~~

<hr>

1 - iterable add_bulk
```rust
use pyo3::prelude::*;
use pyo3::types::PyAny;

#[pyfunction]
fn process_iterable(iterable: &PyAny) -> PyResult<()> {
    // Check if the input is an iterable
    if let Ok(iterator) = iterable.iter() {
        for item in iterator {
            let value: i32 = item?.extract()?;
            println!("{}", value);
        }
    } else {
        return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>("Expected an iterable"));
    }

    Ok(())
}

#[pymodule]
fn mymodule(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(process_iterable, m)?)?;
    Ok(())
}

```