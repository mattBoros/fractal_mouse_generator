import subprocess

location_of_jar = r'image_renderer.jar'

def render_image(c, location):
    command = 'java -jar {0} {1} {2} {3}'.format(location_of_jar,
                                                 str(c.real),
                                                 str(c.imag),
                                                 location)
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    out = p.stdout.readline()
    return out
