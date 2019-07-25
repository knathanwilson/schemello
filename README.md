# schemello
Tool for making advanced text formatting functions.

## token
A token is something that will be replaced. This can be done 2 different ways. You can make a static word replacement like this.
```python
scheme.simpletoken('AMP', '&')
```
You can have a token replacer function as follows:
```python
@scheme.token('AMP')
def replaceme (text, **args): return '&'
```

## bracket
A bracket is is a special text that takes in between text to change them. You can use it to make easy formatting as shown below.
```python
@scheme.bracket('BOLD')
def replaceme (fullline, cut, text, **args): return text.replace(fullline, '<b>' + text + '</b>')
```

## singleline
A singline, markup value.
```python
@scheme.singleline('name')
def replaceme (fullline, cut, text, **args): return text.replace(fullline, 'My name is ' + cut)
```
