//////////////////////////////////////////////////////
// MK Glow Settings Legacy	    	    	        //
//					                                //
// Created by Michael Kremmel                       //
// www.michaelkremmel.de                            //
// Copyright © 2020 All rights reserved.            //
//////////////////////////////////////////////////////

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace MK.Glow.LWRP
{
    internal sealed class SettingsPPSV2 : MK.Glow.Settings
    {
        public static implicit operator SettingsPPSV2(MK.Glow.LWRP.MKGlowLite input)
        {
            SettingsPPSV2 settings = new SettingsPPSV2();
            
            //Main
            settings.debugView = input.debugView;
            settings.workflow = input.workflow;
            settings.selectiveRenderLayerMask = input.selectiveRenderLayerMask;
            settings.anamorphicRatio = input.anamorphicRatio;

            //Bloom
            settings.bloomThreshold = input.bloomThreshold;
            settings.bloomScattering = input.bloomScattering;
            settings.bloomIntensity = input.bloomIntensity;

            //LensSurface
            settings.allowLensSurface = input.allowLensSurface;
            settings.lensSurfaceDirtTexture = input.lensSurfaceDirtTexture;
            settings.lensSurfaceDirtIntensity = input.lensSurfaceDirtIntensity;
            settings.lensSurfaceDiffractionTexture = input.lensSurfaceDiffractionTexture;
            settings.lensSurfaceDiffractionIntensity = input.lensSurfaceDiffractionIntensity;

            return settings;
        }
    }
}
