# Create your views here.
from zlib import compress, decompress
import struct

from django.shortcuts import render_to_response as r2r
from django.template import RequestContext

from twuuenc.tw_uuencode import encode, decode
from twuuenc.web.forms import *


def render(p, v, r):
  return r2r(p, v, context_instance=RequestContext(r))

def index(request):
  input          = None
  input_len      = 0
  output         = None
  output_len     = 0
  compressed     = False
  compressed_len = 0

  if request.method == 'POST':
    form = EncodeForm(request.POST)
    if form.is_valid():
      if form.cleaned_data['input']:
        msg = form.cleaned_data['input'].encode('utf-8')
        input_len = len(msg)
        input = form.cleaned_data['input']
        if form.cleaned_data['compress']:
          compressed = True
          msg = compress(msg, 9)
          compressed_len = len(msg)
        output = ''.join(encode(msg))
        output_len = len(output)

      elif form.cleaned_data['output']:
        output = form.cleaned_data['output']
        output_len = len(output)

        input = decode(output)
        input_len = len(input)

        if form.cleaned_data['compress']:
          compressed_len = input_len
          compressed = True
          input = decompress(input)
          input_len = len(input)
      else:
        print 'nothing included'
    else:
      print 'invalid form'
  else:
    pass # GET

  initial = {
    'input'   : input,
    'output'  : output,
    'compress': compressed,
  }
  form = EncodeForm(initial=initial)

        
  params = {
    'encode_form'     : form,
    'compressed'      : compressed,
    'input_len'       : input_len,
    'output_len'      : output_len,
    'compressed_len'  : compressed_len,
  }
  return render('index.html', params, request)
