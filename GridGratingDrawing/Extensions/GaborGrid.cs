using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;

public struct GaborProperties
{
    public float X;
    public float Y;
    public float Size;
    public float SpatialFrequency;
}

[Combinator]
[Description("Parameterizes and returns a sequence of all the gabor elements in a test grid.")]
[WorkflowElementCategory(ElementCategory.Source)]
public class GaborGrid
{
    public int GridSize { get; set; }

    public float SpatialFrequency { get; set; }

    IEnumerable<GaborProperties> GetGridElements()
    {
        var k = GridSize;
        var sz = 2f / k;
        for (int i = 0; i < k; i++)
        {
            for (int j = 0; j < k; j++)
            {
                yield return new GaborProperties
                {
                    Size = sz,
                    X = j * sz - 1 + sz / 2,
                    Y = i * sz - 1 + sz / 2,
                    SpatialFrequency = SpatialFrequency * k
                };
            }
        }
    }

    public IObservable<GaborProperties> Process()
    {
        return GetGridElements().ToObservable();
    }
}
