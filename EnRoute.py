# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EnRoute
                                 A QGIS plugin
 点列に対するルート検索
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-01-18
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Yoichi Kayama/Aeroasahi corporation
        email                : youichi-kayama@aeroasahi.co.jp
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication,QVariant
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from qgis.core import QgsWkbTypes, QgsGeometry, QgsVectorLayer, QgsField, QgsFeature, QgsMapLayer,QgsProcessingFeedback,QgsProject

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .EnRoute_dialog import EnRouteDialog
import os.path
import processing


class EnRoute:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'EnRoute_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = EnRouteDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&EnRoute')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'EnRoute')
        self.toolbar.setObjectName(u'EnRoute')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('EnRoute', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        ricon_path = ':/plugins/EnRoute/route.png'

        self.add_action(
            ricon_path,
            text=self.tr(u'点列経路探索'),
            callback=self.run,
            parent=self.iface.mainWindow())
            
        icon_path = ':/plugins/EnRoute/icon.png'
        self.add_action(
            ricon_path,
            text=self.tr(u'CSVファイル作成'),
            callback=self.runCSV,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&EnRoute'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        
        
        
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            
            rdlayer = self.dlg.mMapLayerComboBox.currentLayer() # 道路レイヤ
            
            ptlayer = self.dlg.mMapLayerComboBox_2.currentLayer() # 点群レイヤ
 
 
            ABlayer = self.dlg.mMapLayerComboBox_3.currentLayer() # 2点レイヤ
            
            if ( rdlayer is not None and ptlayer is not None and ABlayer is not None):
                 
                                  
 
                 
                 #  2点取得
                 p1, p2 = self.getStartPoint( ABlayer )
                 
                 p1g = p1.geometry()
                 p2g = p2.geometry()
                 
                 features = ptlayer.getFeatures()
                 
                 
                 params = { 'DEFAULT_DIRECTION' : 2, 'DEFAULT_SPEED' : 50, 'DIRECTION_FIELD' : None,'INPUT' : rdlayer, 'OUTPUT' : 'memory:', 'SPEED_FIELD' : None, 'START_POINT' : '-32900.94654466226,-45493.2545761942 [USER:100025]', 'STRATEGY' : 0, 'TOLERANCE' : 0, 'VALUE_BACKWARD' : '', 'VALUE_BOTH' : '', 'VALUE_FORWARD' : '' }
                 
                 # create layer
                 vl = QgsVectorLayer("Line", "temporary_line1", "memory")
                 pr = vl.dataProvider()
                 
                 # add fields
                 pr.addAttributes([QgsField("tid",  QVariant.Int),
                    QgsField("start", QVariant.String),
                    QgsField("end",  QVariant.String),
                    QgsField("cost", QVariant.Double)])
                 vl.updateFields() # tell the vector layer to fetch changes from the provider
                 
                 ip = 1
                 
                 feedback = QgsProcessingFeedback()
                 
                 for pfeature in features:    #点群レイヤのポイントループ
                      egeom = pfeature.geometry()
                      
                      geomSingleType = QgsWkbTypes.isSingleType(egeom.wkbType())
                      
                      if geomSingleType:
                              x = egeom.asPoint()
                              print("Point: ", x)
                              params['END_POINT'] = format( x.x(),'f') + ',' + format(x.y(), 'f')
                              print( params['END_POINT'] )
                              
                      else:
                              x = egeom.asMultiPoint()
                              print("MultiPoint: ", x)
                              params['END_POINT']  = format( x.x(),'f') +',' +  format(x.y(), 'f')
                              
                      #if ip < 10:
                      res = processing.run('qgis:shortestpathpointtopoint', params, feedback=feedback)
                      result_layer = res['OUTPUT']
                      
                      
                              
                      #print(result_layer.isValid())
                              
                      if result_layer.isValid():
                              #          QgsProject.instance().addMapLayer(result_layer)
              
                      
                      
                             nfeatures = result_layer.getFeatures()
                             for nf in nfeatures:    #ルートレイヤのラインループ
                                 tgeom = nf.geometry()
                             
                                # add a feature
                                 fet = QgsFeature(pr.fields())
                                 fet.setGeometry(tgeom)
                                 #fet.setAttributes( QVariant(pfeature['fid']),QVariant(nf['start']),QVariant(nf['end']), QVariant(nf['cost']))
                                 fet['tid'] = pfeature['fid']
                                 fet['start'] = nf['start']
                                 fet['end'] = nf['end']
                                 fet['cost'] = nf['cost']
                                 pr.addFeatures([fet])

                             
                             self.iface.messageBar().pushMessage("EnRoute", params['END_POINT'], level=0, duration=3)
                      else:
                             self.iface.messageBar().pushMessage("EnRoute", 'routing error!', level=0, duration=3)
                      
                      ip = ip + 1
                      
                      del( result_layer )
                      
                      
                 QgsProject.instance().addMapLayer(vl)
                 
                 rdtext = rdlayer.name()
                 self.iface.messageBar().pushMessage("EnRoute", rdtext, level=0, duration=3)
                 
                 
            
            else:
                 self.iface.messageBar().pushMessage("EnRoute", u'レイヤの指定が足りません', level=1, duration=3)
 
            
            pass
            
    def getStartPoint(self, stLayer):
        #    2個の指定点を取得する
    
        p1=QgsFeature() 
        p2=QgsFeature() 
        
        features = stLayer.getFeatures()
        
        
        features.nextFeature(p1)
        features.nextFeature(p2)

        
        return p1, p2
            
    def runCSV(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
            
                        
