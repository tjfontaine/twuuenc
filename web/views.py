# Create your views here.
from zlib import compress, decompress
import struct

from django.shortcuts import render_to_response as r2r
from django.template import RequestContext

from twuuenc.tw_uuencode import encode, decode, TWUUENC_START, TWUUENC_START_ZLIB
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
  form_invalid   = False
  markers        = True

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

        if form.cleaned_data['markers']:
          if compressed:
            output = TWUUENC_START_ZLIB + output + TWUUENC_START_ZLIB
          else:
            output = TWUUENC_START + output + TWUUENC_START

        output_len = len(output)

      elif form.cleaned_data['output']:
        output = form.cleaned_data['output']
        output_len = len(output)
        orig = output

        if form.cleaned_data['markers']:
          end = -1
          start = output.find(TWUUENC_START)
          if start > -1:
            end = output.find(TWUUENC_START, start+1)

          if start > -1 and end > -1:
            output = output[start+1:end-start]
            form.cleaned_data['compress'] = False
            compressed = False
          else:
            start = output.find(TWUUENC_START_ZLIB)
            if start > -1:
              end = output.find(TWUUENC_START_ZLIB, start+1)

            if start > -1 and end > -1:
              output = output[start+1:end-start]
              form.cleaned_data['compress'] = True

        input = decode(output)
        input_len = len(input)

        if form.cleaned_data['compress']:
          compressed_len = input_len
          compressed = True
          input = decompress(input)
          input_len = len(input)

        output = orig
    else:
      form_invalid = True

  initial = {
    'input'   : input,
    'output'  : output,
    'compress': compressed,
    'markers' : markers,
  }

  if not form_invalid:
    form = EncodeForm(initial=initial)

  params = {
    'encode_form'     : form,
    'compressed'      : compressed,
    'input_len'       : input_len,
    'output_len'      : output_len,
    'compressed_len'  : compressed_len,
    'clean_marker'    : TWUUENC_START,
    'zlib_marker'     : TWUUENC_START_ZLIB,
  }
  return render('index.html', params, request)
