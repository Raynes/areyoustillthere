# areyoustillthere

A library for email verification.

* Verify if an email exists on SMTP servers that support this.
* MX record lookup.

## Usage

First of all, get it!

```
pip install areyoustillthere
```

Next, use it!

```python
>>> import ayst
>>> x = ayst.Email('neontrees@gmail.com')
>>> x.validate()
True
>>> x.valid
True
>>> x.servers
['gmail-smtp-in.l.google.com', 'alt1.gmail-smtp-in.l.google.com', 'alt2.gmail-smtp-in.l.google.com', 'alt3.gmail-smtp-in.l.google.com', 'alt4.gmail-smtp-in.l.google.com']
```
