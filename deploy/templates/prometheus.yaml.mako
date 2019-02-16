<%!
    import os
    import sys
    import base64
    from ph_confer import file_mode, file_location
%>\
<%
    file_mode('644')
    file_location('../values/prometheus.yaml')

    run_mode = os.getenv('RUN_MODE')
    if run_mode is None:
      raise Exception('You must set the RUN_MODE variable to one of prod, dev, or test!')
%>\

# TODO