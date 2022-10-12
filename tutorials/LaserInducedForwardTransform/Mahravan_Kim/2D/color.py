# state file generated using paraview version 5.4.1

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [641, 802]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.OrientationAxesVisibility = 0
renderView1.CenterOfRotation = [3.5351756888371726e-06, 3.4231545224324034e-05, 0.0]
renderView1.StereoType = 0
renderView1.CameraPosition = [-7.05078638575575e-07, 8.590158056036023e-05, 0.0003221065709371349]
renderView1.CameraFocalPoint = [-7.05078638575575e-07, 8.590158056036023e-05, 2.5571825324806804e-05]
renderView1.CameraParallelScale = 0.0003162376606983792
renderView1.Background = [1.0, 1.0, 1.0]

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'OpenFOAMReader'
afoam = OpenFOAMReader(FileName='/home/user/OpenFOAM/user-dev/run/LIFT/1_NewSeri_MainCase/a.foam')
afoam.CaseType = 'Decomposed Case'
afoam.MeshRegions = ['internalMesh']
afoam.CellArrays = ['T', 'T.air', 'T.water', 'U', 'alpha.water', 'magGradRho', 'maxGradRho', 'p', 'p_rgh', 'rho']

# create a new 'Slice'
slice1 = Slice(Input=afoam)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [9.99999974737875e-05, 0.000300000014249235, 0.0]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# create a new 'Clip'
clip2 = Clip(Input=slice1)
clip2.ClipType = 'Box'
clip2.Scalars = ['POINTS', 'p']
clip2.Value = 883162.390625
clip2.InsideOut = 1

# init the 'Box' selected for 'ClipType'
clip2.ClipType.Bounds = [0.0, 0.00019999999494757503, 0.0, 0.0006000000284984708, 0.0, 0.0]
clip2.ClipType.Scale = [0.3, 0.25, 1.0]

# create a new 'Threshold'
threshold1 = Threshold(Input=clip2)
threshold1.Scalars = ['CELLS', 'alpha.water']
threshold1.ThresholdRange = [0.5, 1.5]

# create a new 'Glyph'
glyph1 = Glyph(Input=threshold1,
    GlyphType='Arrow')
glyph1.Scalars = ['POINTS', 'p']
glyph1.Vectors = ['POINTS', 'U']
glyph1.ScaleFactor = 5e-06
glyph1.GlyphMode = 'Every Nth Point'
glyph1.MaximumNumberOfSamplePoints = 1000
glyph1.Seed = 5000
glyph1.Stride = 200
glyph1.GlyphTransform = 'Transform2'

# create a new 'Transform'
transform1 = Transform(Input=clip2)
transform1.Transform = 'Transform'

# init the 'Transform' selected for 'Transform'
transform1.Transform.Scale = [-1.0, 1.0, 1.0]

# create a new 'Calculator'
calculator1 = Calculator(Input=transform1)
calculator1.ResultArrayName = 'Normalized pressure'
calculator1.Function = 'p_rgh/200e6'

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get color transfer function/color map for 'Normalizedpressure'
normalizedpressureLUT = GetColorTransferFunction('Normalizedpressure')
normalizedpressureLUT.RGBPoints = [0.0, 0.278431372549, 0.278431372549, 0.858823529412, 0.1430000000000291, 0.0, 0.0, 0.360784313725, 0.2849999999998545, 0.0, 1.0, 1.0, 0.4290000000000873, 0.0, 0.501960784314, 0.0, 0.5709999999999128, 1.0, 1.0, 0.0, 0.7139999999999418, 1.0, 0.380392156863, 0.0, 0.856999999999971, 0.419607843137, 0.0, 0.0, 1.0, 0.878431372549, 0.301960784314, 0.301960784314]
normalizedpressureLUT.ColorSpace = 'RGB'
normalizedpressureLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'Normalizedpressure'
normalizedpressurePWF = GetOpacityTransferFunction('Normalizedpressure')
normalizedpressurePWF.ScalarRangeInitialized = 1

# get color transfer function/color map for 'alphawater'
alphawaterLUT = GetColorTransferFunction('alphawater')
alphawaterLUT.RGBPoints = [-9.212832943319631e-32, 0.6823529411764706, 0.6705882352941176, 0.6901960784313725, 1.0, 0.0, 0.0, 0.0, 1.0, 0.7647058823529411, 0.20392156862745098, 0.9490196078431372]
alphawaterLUT.ColorSpace = 'RGB'
alphawaterLUT.NanColor = [1.0, 0.0, 0.0]
alphawaterLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'alphawater'
alphawaterPWF = GetOpacityTransferFunction('alphawater')
alphawaterPWF.Points = [-9.212832943319631e-32, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
alphawaterPWF.ScalarRangeInitialized = 1

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from clip2
clip2Display = Show(clip2, renderView1)
# trace defaults for the display properties.
clip2Display.Representation = 'Surface'
clip2Display.ColorArrayName = ['POINTS', 'alpha.water']
clip2Display.LookupTable = alphawaterLUT
clip2Display.OSPRayScaleArray = 'p'
clip2Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip2Display.SelectOrientationVectors = 'U'
clip2Display.ScaleFactor = 1.2000000424450263e-05
clip2Display.SelectScaleArray = 'p'
clip2Display.GlyphType = 'Arrow'
clip2Display.GlyphTableIndexArray = 'p'
clip2Display.DataAxesGrid = 'GridAxesRepresentation'
clip2Display.PolarAxes = 'PolarAxesRepresentation'
clip2Display.ScalarOpacityFunction = alphawaterPWF
clip2Display.ScalarOpacityUnitDistance = 1.6795138920840807e-06

# show data from glyph1
glyph1Display = Show(glyph1, renderView1)
# trace defaults for the display properties.
glyph1Display.Representation = 'Surface'
glyph1Display.ColorArrayName = ['POINTS', '']
glyph1Display.OSPRayScaleArray = 'GlyphScale'
glyph1Display.OSPRayScaleFunction = 'PiecewiseFunction'
glyph1Display.SelectOrientationVectors = 'GlyphVector'
glyph1Display.ScaleFactor = 1.2284906534887342e-05
glyph1Display.SelectScaleArray = 'GlyphScale'
glyph1Display.GlyphType = 'Arrow'
glyph1Display.GlyphTableIndexArray = 'GlyphScale'
glyph1Display.DataAxesGrid = 'GridAxesRepresentation'
glyph1Display.PolarAxes = 'PolarAxesRepresentation'

# show data from calculator1
calculator1Display = Show(calculator1, renderView1)
# trace defaults for the display properties.
calculator1Display.Representation = 'Surface'
calculator1Display.ColorArrayName = ['POINTS', 'Normalized pressure']
calculator1Display.LookupTable = normalizedpressureLUT
calculator1Display.OSPRayScaleArray = 'Normalized pressure'
calculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator1Display.SelectOrientationVectors = 'U'
calculator1Display.ScaleFactor = 9.000000136438758e-06
calculator1Display.SelectScaleArray = 'Normalized pressure'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.GlyphTableIndexArray = 'Normalized pressure'
calculator1Display.DataAxesGrid = 'GridAxesRepresentation'
calculator1Display.PolarAxes = 'PolarAxesRepresentation'
calculator1Display.ScalarOpacityFunction = normalizedpressurePWF
calculator1Display.ScalarOpacityUnitDistance = 1.4537713232881765e-06

# show color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# setup the color legend parameters for each legend in this view

# get color legend/bar for normalizedpressureLUT in view renderView1
normalizedpressureLUTColorBar = GetScalarBar(normalizedpressureLUT, renderView1)
normalizedpressureLUTColorBar.Orientation = 'Horizontal'
normalizedpressureLUTColorBar.WindowLocation = 'AnyLocation'
normalizedpressureLUTColorBar.Position = [0.2225619129034006, 0.882992518703242]
normalizedpressureLUTColorBar.Title = 'Normalized pressure'
normalizedpressureLUTColorBar.ComponentTitle = ''
normalizedpressureLUTColorBar.TitleColor = [0.0392156862745098, 0.0392156862745098, 0.0392156862745098]
normalizedpressureLUTColorBar.TitleFontFamily = 'Times'
normalizedpressureLUTColorBar.TitleBold = 1
normalizedpressureLUTColorBar.TitleItalic = 1
normalizedpressureLUTColorBar.TitleFontSize = 20
normalizedpressureLUTColorBar.LabelColor = [0.00784313725490196, 0.00784313725490196, 0.00784313725490196]
normalizedpressureLUTColorBar.LabelFontFamily = 'Times'
normalizedpressureLUTColorBar.LabelBold = 1
normalizedpressureLUTColorBar.LabelItalic = 1
normalizedpressureLUTColorBar.LabelFontSize = 20
normalizedpressureLUTColorBar.ScalarBarLength = 0.5638611449451882

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(clip2)
# ----------------------------------------------------------------