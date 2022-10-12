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
renderView1.ViewSize = [431, 760]
renderView1.AnnotationColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.OrientationAxesVisibility = 0
renderView1.OrientationAxesLabelColor = [0.0, 0.0, 0.0]
renderView1.CenterOfRotation = [0.0, 0.0, 0.00013724951713811606]
renderView1.StereoType = 0
renderView1.CameraPosition = [-3.990137307402311e-05, 0.0005082967249139011, 1.3930236662343841e-05]
renderView1.CameraFocalPoint = [-5.977333843391804e-06, 7.800139019301549e-05, 0.00011209087577738386]
renderView1.CameraViewUp = [0.003663800523366141, -0.22213403885302477, -0.9750092539809907]
renderView1.CameraParallelScale = 0.00044246665342556396
renderView1.Background = [1.0, 1.0, 1.0]

# init the 'GridAxes3DActor' selected for 'AxesGrid'
renderView1.AxesGrid.XTitleColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.YTitleColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.XLabelColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.YLabelColor = [0.0, 0.0, 0.0]
renderView1.AxesGrid.ZLabelColor = [0.0, 0.0, 0.0]

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'OpenFOAMReader'
afoam = OpenFOAMReader(FileName='a.foam')
afoam.CaseType = 'Decomposed Case'
afoam.MeshRegions = ['internalMesh']
afoam.CellArrays = ['T', 'T.air', 'T.water', 'U', 'alpha.water', 'magGradRho', 'maxGradRho', 'p', 'p_rgh', 'rho']

# create a new 'Box'
box1 = Box()
box1.XLength = 2e-05
box1.YLength = 1e-06
box1.ZLength = 2e-06
box1.Center = [4e-05, 0.0, 0.00015]

# create a new 'Slice'
slice1 = Slice(Input=afoam)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [9.99999974737875e-05, 0.000300000014249235, 0.0]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# create a new 'Contour'
contour1 = Contour(Input=slice1)
contour1.ContourBy = ['POINTS', 'alpha.water']
contour1.Isosurfaces = [0.5]
contour1.PointMergeMethod = 'Uniform Binning'

# create a new 'Transform'
transform1 = Transform(Input=contour1)
transform1.Transform = 'Transform'

# init the 'Transform' selected for 'Transform'
transform1.Transform.Rotate = [90.0, 0.0, 0.0]

# create a new 'Rotational Extrusion'
rotationalExtrusion1 = RotationalExtrusion(Input=transform1)
rotationalExtrusion1.Resolution = 200

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from rotationalExtrusion1
rotationalExtrusion1Display = Show(rotationalExtrusion1, renderView1)
# trace defaults for the display properties.
rotationalExtrusion1Display.Representation = 'Surface'
rotationalExtrusion1Display.ColorArrayName = ['POINTS', '']
rotationalExtrusion1Display.DiffuseColor = [0.0, 0.0, 0.0]
rotationalExtrusion1Display.Opacity = 0.6
rotationalExtrusion1Display.OSPRayScaleArray = 'p'
rotationalExtrusion1Display.OSPRayScaleFunction = 'PiecewiseFunction'
rotationalExtrusion1Display.SelectOrientationVectors = 'U'
rotationalExtrusion1Display.ScaleFactor = 3.9999998989515007e-05
rotationalExtrusion1Display.SelectScaleArray = 'p'
rotationalExtrusion1Display.GlyphType = 'Arrow'
rotationalExtrusion1Display.GlyphTableIndexArray = 'p'
rotationalExtrusion1Display.DataAxesGrid = 'GridAxesRepresentation'
rotationalExtrusion1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
rotationalExtrusion1Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1940530048.0, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
rotationalExtrusion1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
rotationalExtrusion1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
rotationalExtrusion1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
rotationalExtrusion1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
rotationalExtrusion1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
rotationalExtrusion1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
rotationalExtrusion1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
rotationalExtrusion1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
rotationalExtrusion1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
rotationalExtrusion1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# show data from box1
box1Display = Show(box1, renderView1)
# trace defaults for the display properties.
box1Display.Representation = 'Surface'
box1Display.ColorArrayName = [None, '']
box1Display.DiffuseColor = [0.0, 0.0, 0.0]
box1Display.OSPRayScaleArray = 'Normals'
box1Display.OSPRayScaleFunction = 'PiecewiseFunction'
box1Display.SelectOrientationVectors = 'None'
box1Display.ScaleFactor = 1.9999999494757505e-06
box1Display.SelectScaleArray = 'None'
box1Display.GlyphType = 'Arrow'
box1Display.GlyphTableIndexArray = 'None'
box1Display.DataAxesGrid = 'GridAxesRepresentation'
box1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
box1Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1940530048.0, 1.0, 0.5, 0.0]

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
box1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
box1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
box1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
box1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
box1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
box1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
box1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
box1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
box1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
box1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(box1)
# ----------------------------------------------------------------

times=[4e-07, 1.2e-06, 1.5e-06, 2e-06, 2.5e-06, 4e-06]

for t in times:
    renderView1.ViewTime = t
    SaveScreenshot("3D/3D"+str(t)+".jpg", magnification=2.5, quality=100, view=renderView1)

	# ~ WriteImage("3D"+str(t)+".jpg",dpi=2000)
