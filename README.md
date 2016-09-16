# eet-cz
Czech tax office communication

## Install
```
pip install git+https://github.com/euroska/eet-cz.git
```
 
## Example
### Test
```python
>>> from eet import EETRequest
>>> t = EETRequest.test()
>>> r = t.send()
>>> r.fik
'8415fba2-759a-4303-b0a0-88fff30bc8b7-ff'
```

### Release
```python
>>> from eet import EETRequest, EETConfig
>>> c = EETConfig('CZ00000019', 235, 'asdsa', key_file='key.pem', cert_file='cert.pem', root_cert_file='root_cert.pem')
>>> t = EETRequest(c, price_sum=34113.00, price_sum_normal_vat=100, normal_vat_sum=21, number='0/6460/ZQ42')
>>> r = t.send()
>>> r.fik
'0db04b7c-86e1-4485-be36-076b78898f2d-ff'
```



